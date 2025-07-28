from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect
from app import db
from app.models import FuelRequest, Vehicle 
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from sqlalchemy import extract, func
from datetime import datetime
from app.models import FuelRequest
from app.models import Vehicle

fuelrequest_bp = Blueprint('fuelrequest', __name__, url_prefix='/fuelrequest')



# create fuel request
@fuelrequest_bp.route('/request_fuel', methods=['GET', 'POST'])
@login_required
@role_required('Driver')
def request_fuel():
    if request.method == 'POST':
        print("Received form data:", request.form)
        for key in request.form:
            print(f"{key}: {request.form[key]}")
        try:
            driver_name = current_user.full_name
            vehicle_id = int(request.form.get('vehicle_id'))
            card_no = request.form.get('card_no')
            odometer_reading = float(request.form.get('odometer_reading'))
            office_officer_assigned = request.form.get('office_officer_assigned')
            amount_requested = float(request.form.get('amount_requested'))
            amount_last_loaded = float(request.form.get('amount_last_loaded'))
            current_card_balance = float(request.form.get('current_card_balance'))
            
            if not vehicle_id or not amount_requested:
                flash('Vehicle and amount requested are required.', 'danger')
                return redirect(url_for('driver.request_fuel'))

            new_request = FuelRequest(
                user_id=current_user.id,
                driver_name=driver_name,
                vehicle_id=vehicle_id,
                card_no=card_no,
                odometer_reading=odometer_reading,
                office_officer_assigned=office_officer_assigned,
                amount_requested=amount_requested,
                amount_last_loaded=amount_last_loaded,
                current_card_balance=current_card_balance,
                status='Submitted',
                created_at=datetime.utcnow()
            )

            db.session.add(new_request)
            db.session.commit()
            print("Fuel request saved:", new_request.id)
            flash('Fuel request submitted successfully.', 'success')
            return redirect(url_for('fuelrequest.request_fuel'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('fuelrequest.request_fuel'))
    print("Received form data:", request.form)

    vehicles = Vehicle.query.all()
    return render_template('fuel/request_form.html', vehicles=vehicles)


# Approve fuel request (Approver)
@fuelrequest_bp.route('/approve/<int:request_id>', methods=['POST'])
@login_required
@role_required('Approver')
def approve_request(request_id):
    req = FuelRequest.query.get_or_404(request_id)
    if req.status == 'Submitted':
        req.status = 'Approved'
        req.approved_at = datetime.utcnow()
        db.session.commit()
        flash('Request approved successfully!', 'success')
    else:
        flash('Request is already approved.', 'warning')
    return redirect(url_for('fuelrequest.approver_dashboard'))


@fuelrequest_bp.route('/cancel_request/<int:request_id>', methods=['POST'])
@login_required
@role_required('Approver')
def cancel_request(request_id):
    req = FuelRequest.query.get_or_404(request_id)
    req.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('fuelrequest.approver_dashboard'))


@fuelrequest_bp.route('/approver_dashboard')
@login_required
@role_required('Approver')
def approver_dashboard():
    from sqlalchemy import extract

    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    # Pending fuel requests (submitted, awaiting approval)
    pending_requests = FuelRequest.query.filter_by(status='Submitted').all()

    # Approved but not yet loaded
    approved_requests = FuelRequest.query.filter_by(status='Approved').all()

    # All records (Approved, Loaded, Rejected)
    all_records = FuelRequest.query.filter(FuelRequest.status.in_(['Loaded', 'Rejected'])).all()

    # Count totals for cards
    approved_this_month = FuelRequest.query.filter(
        FuelRequest.status == 'Approved',
        extract('month', FuelRequest.created_at) == current_month,
        extract('year', FuelRequest.created_at) == current_year
    ).count()

    total_requests = FuelRequest.query.count()

    return render_template(
        'dashboards/approver_dashboard.html',
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        all_records=all_records,
        approved_count=approved_this_month,
        total_requests=total_requests
    )
    
# approvers view route
@fuelrequest_bp.route('/view_request/<int:request_id>')
@login_required
@role_required('Approver')
def view_request(request_id):
    req = FuelRequest.query.get_or_404(request_id)
    return render_template('fuel/view_request.html', request=req)

@fuelrequest_bp.route('/approved')
@login_required
@role_required('Approver')
def approved_records():
    approved_requests = FuelRequest.query.filter_by(status='Approved').all()
    return render_template('approver/approver_approved.html', approved_requests=approved_requests)

# aprrovers search route
@fuelrequest_bp.route('/approver/records', methods=['GET'])
@login_required
@role_required('Approver')
def view_approver_records():
    search_query = request.args.get('search', '').strip()

    query = FuelRequest.query.filter(FuelRequest.status.in_(['Approved', 'Loaded', 'Rejected']))

    if search_query:
        query = query.join(Vehicle).filter(
            (FuelRequest.driver_name.ilike(f'%{search_query}%')) |
            (Vehicle.registration_no.ilike(f'%{search_query}%'))
        )

    records = query.order_by(FuelRequest.created_at.desc()).all()

    return render_template('approver/approver_records.html', records=records)

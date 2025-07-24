from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models import FuelRequest, FuelCardRecord
from app import db
from app.models import FuelRequest, Vehicle
from datetime import datetime

# Blueprint setup
loader_bp = Blueprint('loader_module', __name__, url_prefix='/loader')

# Loader dashboard showing pending and all requests
@loader_bp.route('/dashboard')
@login_required
@role_required('Loader')
def dashboard():
    approved_requests = FuelRequest.query.filter_by(status='Approved').all()
    all_requests = FuelRequest.query.all()
    return render_template(
        'dashboards/loader_dashboard.html',
        approved_requests=approved_requests,
        all_requests=all_requests
    )

@loader_bp.route('/load_request/<int:request_id>', methods=['POST'])
@login_required
@role_required('Loader')
def load_request(request_id):
    req = FuelRequest.query.get_or_404(request_id)

    try:
        # Get amount loaded from the form
        amount_loaded = float(request.form.get('amount_loaded'))
        if amount_loaded <= 0:
            flash("Loaded amount must be greater than 0.", "danger")
            return redirect(url_for('loader_module.dashboard'))

        balance_before = float(req.current_card_balance or 0)
        balance_after = balance_before + amount_loaded

        # Ensure card_no is present
        card_no = req.card_no if hasattr(req, 'card_no') and req.card_no else 'N/A'

        # Create fuel card record
        record = FuelCardRecord(
            request_id=request_id,
            card_no=card_no,
            amount_loaded=amount_loaded,
            balance_before=balance_before,
            balance_after=balance_after,
            loaded_by=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(record)

        # Update the fuel request
        req.status = 'Loaded'
        req.amount_loaded = amount_loaded  # You may rename to amount_loaded
        req.current_card_balance = balance_after
        req.loaded_at = datetime.utcnow()

        db.session.commit()

        flash(f'Request marked as loaded with {amount_loaded} Ksh.', 'success')
        return redirect(url_for('loader_module.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error loading fuel: {str(e)}', 'danger')
        return redirect(url_for('loader_module.dashboard'))



# Mark fuel request as loaded
@loader_bp.route('/load_fuel/<int:request_id>', methods=['POST'])
@login_required
@role_required('Loader')
def load_fuel(request_id):
    fuel_request = FuelRequest.query.get_or_404(request_id)

    try:
        #get loaders input
        amount_loaded = float(request.form.get('amount_loaded',0))
        if amount_loaded <= 0:
            flash('Please enter a valid amount.', 'warning')
            return redirect(url_for('loader_module.dashboard'))
    
        card_no = fuel_request.card_no

        # Calculate balance
        balance_before = float(fuel_request.current_card_balance or 0)
        balance_after = balance_before + amount_loaded

        # Create and save record
        record = FuelCardRecord(
            request_id=request_id,
            card_no=card_no,
            amount_loaded=amount_loaded,
            balance_before=balance_before,
            balance_after=balance_after,
            loaded_by=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(record)

        # Update request
        fuel_request.status = 'Loaded'
        fuel_request.amount_last_loaded = amount_loaded
        fuel_request.current_card_balance = (balance_after)
        fuel_request.loaded_at = datetime.utcnow()
        

        db.session.commit()
        flash('Fuel marked as loaded successfully.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error loading fuel: {str(e)}', 'danger')

    return redirect(url_for('loader_module.dashboard'))

# Reject fuelrequests
@loader_bp.route('/reject_fuel/<int:request_id>', methods=['POST'])
@login_required
@role_required('Loader')
def reject_fuel(request_id):
    fuel_request = FuelRequest.query.get_or_404(request_id)

    try:
        fuel_request.status = 'Rejected'
        fuel_request.loaded_at = datetime.utcnow()
        db.session.commit()
        flash('Fuel request rejected.', 'warning')

    except Exception as e:
        db.session.rollback()
        flash(f'Error rejecting request: {str(e)}', 'danger')

    return redirect(url_for('loader_module.dashboard'))


# View records for loader


@loader_bp.route('/view_records', methods=['GET'])
@login_required
@role_required('Loader')
def view_records():
    search_query = request.args.get('search', '')

    # Filter only approved, loaded, or rejected records
    query = FuelRequest.query.filter(FuelRequest.status.in_(['Approved', 'Loaded', 'Rejected']))

    if search_query:
        query = query.join(Vehicle).filter(
            (FuelRequest.driver_name.ilike(f"%{search_query}%")) |
            (Vehicle.registration_no.ilike(f"%{search_query}%"))
        )

    records = query.order_by(FuelRequest.created_at.desc()).all()
    return render_template('loader/loader_records.html', records=records)


# vehicle adding and deleteing
@loader_bp.route('/register_vehicle', methods=['GET', 'POST'])
@login_required
@role_required('Loader')
def register_vehicle():
    if request.method == 'POST':
        registration_no = request.form['registration']
        department = request.form['department']
        card_no = request.form['card_no']
        model = request.form['model']
        color = request.form['color']

        # Check uniqueness of card number
        existing_card = Vehicle.query.filter_by(card_no=card_no).first()
        if existing_card:
            flash("Card number already exists.", "danger")
            return redirect(url_for('loader_module.register_vehicle'))

        new_vehicle = Vehicle(
            registration_no=registration_no,
            department=department,
            card_no=card_no,
            model=model,
            color=color
        )
        db.session.add(new_vehicle)
        db.session.commit()
        flash("Vehicle registered successfully!", "success")
        return redirect(url_for('loader_module.register_vehicle'))
    
        # Handle search
    search_query = request.args.get('search', '').strip()
    if search_query:
        vehicles = Vehicle.query.filter(
            (Vehicle.registration_no.ilike(f'%{search_query}%')) |
            (Vehicle.model.ilike(f'%{search_query}%')) |
            (Vehicle.card_no.ilike(f'%{search_query}%'))
        ).all()
    else:
        vehicles = Vehicle.query.all()
    return render_template('dashboards/register_vehicle.html', vehicles=vehicles)


@loader_bp.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
@login_required
@role_required('Loader')
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash("Vehicle deleted successfully.", "success")
    return redirect(url_for('loader_module.register_vehicle'))

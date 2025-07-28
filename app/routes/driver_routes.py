# First, let's update the `driver_dashboard` and `driver_records` views.
# These assume you are using SQLAlchemy and Flask-Login.

# In `driver_routes.py`, update your dashboard and records routes like this:

from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import FuelRequest, Vehicle
from app.utils.decorators import role_required
from datetime import datetime, timedelta

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/driver/dashboard')
@login_required
@role_required('Driver')
def driver_dashboard():

    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    all_requests = FuelRequest.query.filter_by(user_id=current_user.id).order_by(FuelRequest.created_at.desc()).all()
    
    
    print("TOTAL REQUESTS:", len(all_requests))
    for r in all_requests:
        print(r.status, r.vehicle_id)
        
    pending = [r for r in all_requests if r.status in ['Submitted', 'Approved']]
    recent_loaded = [r for r in all_requests if r.status == ['Rejected', 'Loaded'] and r.updated_at >= one_hour_ago]
    print("PENDING:", len(pending))
    print("RECENT LOADED:", len(recent_loaded))
    return render_template('dashboards/driver_dashboard.html', pending=pending, recent_loaded=recent_loaded)

@driver_bp.route('/view_records')
@login_required
@role_required('Driver')
def driver_records():
    # Search filters
    search_reg = request.args.get('search_reg', '').strip()
    search_date = request.args.get('search_date', '').strip()

    # Start query for Loaded records only
    query = FuelRequest.query.filter_by(user_id=current_user.id, status='Loaded')
    if search_reg:
        query = query.join(Vehicle).filter(Vehicle.registration_no.ilike(f'%{search_reg}%'))

    if search_date:
        try:
            date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(FuelRequest.created_at) == date_obj)
        except ValueError:
            pass

    records = query.order_by(FuelRequest.created_at.desc()).all()
    return render_template('fuel/driver_records.html', records=records)


# fetch card number
@driver_bp.route('/get_card_no/<int:vehicle_id>')
@login_required
def get_card_no(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return jsonify({'card_no': vehicle.card_no})
    return jsonify({'error': 'Vehicle not found'}), 404

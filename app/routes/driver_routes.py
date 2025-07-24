# First, let's update the `driver_dashboard` and `driver_records` views.
# These assume you are using SQLAlchemy and Flask-Login.

# In `driver_routes.py`, update your dashboard and records routes like this:

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from app import db
from app.models import FuelRequest, Vehicle
from app.utils.decorators import role_required
from datetime import datetime

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/driver/dashboard')
@login_required
@role_required('Driver')
def driver_dashboard():
    # Show Submitted and Approved requests (not Loaded or Rejected)
    pending_requests = FuelRequest.query.filter(
        FuelRequest.driver_name == current_user.id,
        FuelRequest.status.in_(['Submitted', 'Approved'])
    ).order_by(FuelRequest.created_at.desc()).all()

    return render_template('driver/dashboard.html', pending_requests=pending_requests)

@driver_bp.route('/view_records')
@login_required
@role_required('Driver')
def driver_records():
    # Search filters
    search_reg = request.args.get('search_reg', '').strip()
    search_date = request.args.get('search_date', '').strip()

    # Start query for Loaded records only
    query = FuelRequest.query.filter_by(driver_name=current_user.id, status='Loaded')

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



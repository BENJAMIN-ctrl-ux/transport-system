from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect
from app import db
from app.models import FuelRequest, Vehicle 
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from datetime import datetime

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/driver/dashboard')
@login_required
@role_required('Driver')
def driver_dashboard():
    return render_template('driver/dashboard.html')

@driver_bp.route('/view_records')
@login_required
@role_required('Driver')
def driver_records():
    search_reg = request.args.get('search_reg', '').strip()
    search_date = request.args.get('search_date', '').strip()
    
    query = FuelRequest.query.filter_by(driver_name=current_user.id)
    
    if search_reg:
        query = query.join(Vehicle).filter(Vehicle.registration_no.ilike(f'%{search_reg}%'))

    if search_date:
        try:
            date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(FuelRequest.created_at) == date_obj)
        except ValueError:
            pass  # Ignore invalid dates

    records = query.order_by(FuelRequest.created_at.desc()).all()

    return render_template('fuel/driver_records.html', records=records)

from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/driver/dashboard')
@login_required
@role_required('Driver')
def driver_dashboard():
    return render_template('driver/dashboard.html')

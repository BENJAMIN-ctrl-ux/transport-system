from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required

approver_bp = Blueprint('approver_bp', __name__, url_prefix='/approver')

@approver_bp.route('/dashboard')
@login_required
@role_required('Approver')
def approver_dashboard():
    return render_template('dashboards/approver_dashboard.html')


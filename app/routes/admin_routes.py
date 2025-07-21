from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required  

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('Administrator')
def admin_dashboard():
    return render_template('admin/dashboard.html')

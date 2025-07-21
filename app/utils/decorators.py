from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role.name in roles:
                return view_func(*args, **kwargs)
            flash("Unauthorized access.", "danger")
            return redirect(url_for('auth.login'))  
        return wrapped_view
    return decorator

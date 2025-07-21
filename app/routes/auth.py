# app/auth.py
from flask import Blueprint, request, jsonify, session
from flask_login import login_user
from app import db
from app.models import User
from werkzeug.security import check_password_hash
from datetime import datetime
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.password == password:  # In production use hashed passwords!
        login_user(user)
        return jsonify({'message': f'Welcome {user.username}', 'role': user.role.name})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(
        username=data.get('username'),
        email=data.get('email'),
        role_id=data.get('role_id'),
        department_id=data.get('department_id'),
        created_at=datetime.utcnow()
    )
    user.set_password(data.get('password'))

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login'))

            if current_user.role.name not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('main.index'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

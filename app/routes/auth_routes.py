from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Role
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')

            # Redirect based on role
            if user.role.name == 'Driver':
                return redirect(url_for('driver.driver_dashboard'))
            elif user.role.name == 'Approver':
                return redirect(url_for('fuelrequest.approver_dashboard'))
            elif user.role.name == 'Loader':
                return redirect(url_for('loader_module.dashboard'))
            elif user.role.name == 'Administrator':
                return redirect(url_for('admin.dashboard'))
            else:
                flash('No dashboard found for your role.', 'warning')
                return redirect(url_for('main.dashboard'))

        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')  # GET request will render this

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        role_name = request.form['role']  # dropdown for role
        
        role = Role.query.filter_by(name=role_name).first()
        
        if not role:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.signup'))

        user = User(username=username,
                    full_name=full_name,
                    email=email,
                    password=generate_password_hash(password),
                    role=role)
        
        
        
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    roles = Role.query.all()
    return render_template('signup.html', roles=roles)

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

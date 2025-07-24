from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Enums
class UserRole(Enum):
    DRIVER = 'driver'
    APPROVER = 'approver'
    LOADER = 'loader'
    ADMIN = 'admin'

class RequestStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    LOADED = 'loaded'
    CANCELLED = 'cancelled'

class ApprovalStatus(Enum):
    APPROVED = 'approved'
    REJECTED = 'rejected'

class LoadingStatus(Enum):
    LOADED = 'loaded'
    CANCELLED = 'cancelled'

# Department
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    users = db.relationship('User', backref='department')
    vehicles = db.relationship('Vehicle', backref='department')

# Role
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', back_populates='role')

# User
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    role = db.relationship('Role', back_populates='users')

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_active(self):
        return True

    def __repr__(self):
        return f'<User {self.username}>'


# Vehicle
class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.String(50), unique=True, nullable=False)  # vehicle_id
    card_no = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    department = db.relationship('Department', backref='vehicles', lazy=True)

    def __repr__(self):
        return f'<Vehicle {self.registration_no}>'

# Fuel Request
class FuelRequest(db.Model):
    __tablename__ = 'fuel_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_name = db.Column(db.String(120))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    card_no = db.Column(db.String(50), nullable=False)
    odometer_reading = db.Column(db.Float, nullable=False)
    office_officer_assigned = db.Column(db.String(120))
    amount_requested = db.Column(db.Float, nullable=False)
    amount_loaded = db.Column(db.Float, nullable=True)
    amount_last_loaded = db.Column(db.Float, nullable=True)
    current_card_balance = db.Column(db.Float)
    status = db.Column(db.String(20), default='Submitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    amount_loaded = db.Column(db.String(20))

    user = db.relationship('User', back_populates='fuel_requests') 
    vehicle = db.relationship('Vehicle', back_populates='fuel_requests')
    driver = db.relationship('User')

# Fuel Approval
class FuelApproval(db.Model):
    __tablename__ = 'fuel_approvals'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('fuel_requests.id'))
    approver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Enum(ApprovalStatus))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    request = db.relationship('FuelRequest')
    approver = db.relationship('User')

# Fuel Loading
class FuelLoading(db.Model):
    __tablename__ = 'fuel_loadings'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('fuel_requests.id'))
    loader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loaded_amount = db.Column(db.Float, nullable=False)
    previous_balance = db.Column(db.Float, nullable=False)
    new_balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(LoadingStatus), default=LoadingStatus.LOADED)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    request = db.relationship('FuelRequest')
    loader = db.relationship('User')
    

class FuelCardRecord(db.Model):
    __tablename__ = 'fuel_card_records'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('fuel_requests.id'), nullable=False)
    amount_loaded = db.Column(db.Float, nullable=False)
    balance_before = db.Column(db.Float, nullable=False)
    balance_after = db.Column(db.Float, nullable=False)
    loaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    card_no = db.Column(db.String(100), nullable=True)

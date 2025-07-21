from app.extensions import db
from app.models.user import User
from app.models.role import Role
from .user import User
from .role import Role
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash





class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    parent_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('email', name='uq_departments_email'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(50))
    card_no = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(100))
    color = db.Column(db.String(50))
    department = db.Column(db.String(100), nullable=False)
    requests = db.relationship('FuelRequest', backref='vehicle', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('registration_no', name='uq_vehicles_plate_number'),
    )


class FuelRequest(db.Model):
    __tablename__ = 'fuel_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    card_no = db.Column(db.String(50), nullable=False)
    odometer_reading = db.Column(db.Float, nullable=True)
    office_officer_assigned = db.Column(db.String(120))

    status = db.Column(db.String(50), default='Submitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    loaded_at = db.Column(db.DateTime, nullable=True)

    amount_requested = db.Column(db.Float, nullable=False)
    amount_last_loaded = db.Column(db.Float, nullable=True)
    current_card_balance = db.Column(db.String(100), nullable=True)

    card_record = db.relationship('FuelCardRecord', uselist=False, backref='fuel_request')


class FuelCardRecord(db.Model):
    __tablename__ = 'fuel_card_records'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('fuel_requests.id'))
    card_no = db.Column(db.String(100), nullable=True)
    amount_loaded = db.Column(db.Float, nullable=False)
    balance_before = db.Column(db.Float, nullable=False)
    balance_after = db.Column(db.Float, nullable=False)
    loaded_by = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_loaded_by_user'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

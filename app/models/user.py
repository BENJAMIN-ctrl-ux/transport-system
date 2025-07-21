from datetime import datetime
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', back_populates='users')
    department = db.relationship('Department', backref='users')
    fuel_card_loads = db.relationship('FuelCardRecord', backref='loader', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('username', name='uq_users_username'),
        db.UniqueConstraint('email', name='uq_users_email'),
    )

    # Flask-Login requirement
    @property
    def is_active(self):
        return True

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_password(self, password):
        return self.check_password(password)

    def __repr__(self):
        return f'<User {self.username}>'

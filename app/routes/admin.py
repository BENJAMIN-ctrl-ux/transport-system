from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Role
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Create a new user
@admin_bp.route('/create-user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    if not all([username, email, password, role_id]):
        return jsonify({'error': 'All fields are required'}), 400

    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role_id=role_id,
        created_at=datetime.utcnow()
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201

# List all users
@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role.name if u.role else None,
            'created_at': u.created_at
        } for u in users
    ])

# Delete (or deactivate) user
@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify

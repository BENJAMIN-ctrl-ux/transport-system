from flask import Blueprint, request, jsonify
from app import db
from app.models import Vehicle

vehicle_bp = Blueprint('vehicle', __name__)

# Add a vehicle via JSON API
@vehicle_bp.route('/add', methods=['POST'])
def add_vehicle():
    data = request.json
    registration_no = data.get('registration_no')
    card_no = data.get('card_no')
    model = data.get('model')
    color = data.get('color')
    department = data.get('department')

    if not registration_no or not card_no:
        return jsonify({'error': 'Registration number and card number are required'}), 400

    # Check for existing card number
    existing = Vehicle.query.filter_by(card_no=card_no).first()
    if existing:
        return jsonify({'error': 'Card number already exists'}), 409

    vehicle = Vehicle(
        registration_no=registration_no,
        card_no=card_no,
        model=model,
        color=color,
        department=department
    )
    db.session.add(vehicle)
    db.session.commit()

    return jsonify({'message': 'Vehicle added successfully', 'vehicle_id': vehicle.id}), 201


# List all vehicles
@vehicle_bp.route('/all', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([
        {
            'id': v.id,
            'registration_no': v.registration_no,
            'card_no': v.card_no,
            'model': v.model,
            'color': v.color,
            'department': v.department
        } for v in vehicles
    ])


# Get vehicle by ID
@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        'id': v.id,
        'registration_no': v.registration_no,
        'card_no': v.card_no,
        'model': v.model,
        'color': v.color,
        'department': v.department
    })

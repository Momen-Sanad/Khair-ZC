from flask import Blueprint, request, jsonify
#from auth_login import token_required 
# from create_event import create
registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['POST'])
#@token_required  # Ensure the user is authenticated

def register_user_for_event():
    from models.dbSchema import db, User, Event, RegisteredEvent
    
    """
    API endpoint to register a user for an event.
    Requires user authentication.
    """
    data = request.json
    event_id = data.get('event_id')
    current_id = data.get('current_id')
    if not event_id:
        return jsonify({'error': 'Event ID is required'}), 400

    # Check if the event exists
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Check if the user is already registered for the event
    existing_registration = RegisteredEvent.query.filter_by(user_id=current_id, event_id=event_id).first()
    if existing_registration:
        # User is already registered
        return jsonify({'error': 'User is already registered for this event'}), 400

    # Check event capacity
    registered_count = RegisteredEvent.query.filter_by(event_id=event_id).count()
    if registered_count >= event.capacity:
        # Insufficient capacity
        return jsonify({'error': 'Event capacity reached'}), 400

    # Register the user for the event
    new_registration = RegisteredEvent(user_id=current_id, event_id=event_id)
    db.session.add(new_registration)
    db.session.commit()
    # Return success msg
    return jsonify({'message': 'User successfully registered for the event'}), 201

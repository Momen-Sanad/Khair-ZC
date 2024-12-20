from flask import Blueprint, request, jsonify
from Security import session_required, admin_required
from models.Notifications import ErrorProcessor

registration_bp = Blueprint('registration', __name__)
Notifications = ErrorProcessor()

@registration_bp.route('/register', methods=['POST'])
@session_required
def register_user_for_campaign():
    from models.dbSchema import db, User, campaign, Registeredcampaign

    """
    API endpoint to register a user for a campaign.
    Requires user authentication.
    """
    data = request.json
    campaign_id = data.get('campaign_id')
    current_id = data.get('current_id')

    if not campaign_id:
        return jsonify(Notifications.process_error("campaign_id_missing")), 400

    # Check if the campaign exists
    campaign = campaign.query.get(campaign_id)
    if not campaign:
        return jsonify(Notifications.process_error("campaign_not_found")), 404

    # Check if the user is already registered for the campaign
    existing_registration = Registeredcampaign.query.filter_by(user_id=current_id, campaign_id=campaign_id).first()
    if existing_registration:
        return jsonify(Notifications.process_error("user_already_registered")), 400

    # Check campaign capacity
    registered_count = Registeredcampaign.query.filter_by(campaign_id=campaign_id).count()
    if registered_count >= campaign.capacity:
        return jsonify(Notifications.process_error("campaign_full")), 400

    # Register the user for the campaign
    new_registration = Registeredcampaign(user_id=current_id, campaign_id=campaign_id)
    db.session.add(new_registration)
    db.session.commit()

    return jsonify(Notifications.process_error("registration_success")), 201

@registration_bp.route('/remove_user', methods=['POST'])
@session_required
@admin_required
def remove_user_from_campaign():
    from models.dbSchema import db, Registeredcampaign

    """
    API endpoint to remove a user from a campaign.
    Requires user authentication.
    """
    data = request.json
    campaign_id = data.get('campaign_id')
    current_id = data.get('current_id')

    if not campaign_id:
        return jsonify(Notifications.process_error("campaign_id_missing")), 400

    # Find the registration entry for the user in the campaign
    registration = Registeredcampaign.query.filter_by(user_id=current_id, campaign_id=campaign_id).first()
    if not registration:
        return jsonify(Notifications.process_error("user_not_registered")), 404

    # Remove the user from the campaign
    db.session.delete(registration)
    db.session.commit()

    return jsonify(Notifications.process_error("removal_success")), 200

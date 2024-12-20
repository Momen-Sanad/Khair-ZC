from flask import Blueprint, request, jsonify
from models.dbSchema import db, Charity, FollowedCharity
from Security import session_required
from models.Notifications import ErrorProcessor

join_bp = Blueprint('join', __name__)
Notifications = ErrorProcessor()

@join_bp.route('/charity', methods=['POST'])  # route is /join/charity
@session_required
def join_charity():
    user_id = request.json.get('user_id')
    charity_id = request.json.get('charity_id')

    if not user_id:
        return jsonify(Notifications.process_error("user_id_required")), 400

    if not charity_id:
        return jsonify(Notifications.process_error("charity_id_required")), 400

    # Check if the charity exists
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify(Notifications.process_error("charity_not_found")), 404

    # Check if the user already follows the charity
    if FollowedCharity.query.filter_by(user_id=user_id, charity_id=charity_id).first():
        return jsonify(Notifications.process_error("already_following_charity")), 400

    # Create a new FollowedCharity object
    followed_charity = FollowedCharity(user_id=user_id, charity_id=charity_id)

    # Add the new FollowedCharity object to the database
    db.session.add(followed_charity)
    db.session.commit()
    return jsonify({"message": "User successfully followed the charity"}), 200

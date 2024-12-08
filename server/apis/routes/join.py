from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity, FollowedCharity

join_bp = Blueprint('join', __name__)


@join_bp.route('/charity', methods=['POST'])  # route is /join/charity
def join_charity():
    user_id = request.json.get('user_id')
    charity_id = request.json.get('charity_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if not charity_id:
        return jsonify({"error": "Charity ID is required"}), 400

    # Check if the charity exists
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found"}), 404

    if FollowedCharity.query.filter_by(user_id=user_id, charity_id=charity_id).first():
        return jsonify({"error": "User already follows this charity"}), 400

    # Create a new FollowedCharity object
    followed_charity = FollowedCharity(user_id=user_id, charity_id=charity_id)

    # Add the new FollowedCharity object to the database
    db.session.add(followed_charity)
    db.session.commit()
    return jsonify({"message": "User successfully followed the charity"}), 200

from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity


serach_bp = Blueprint('search', __name__)

# two search endpoints, one for charities and one for events


@serach_bp.route('/charity', methods=['GET'])  # route is /search/charity
def search_charity():
    # search by name and filter by category (optional)
    name = request.json.get('name')
    category = request.json.get('category')
    charities = []

    if not name:
        return jsonify({"error": "Missing data"}), 400

    if category:
        charities = Charity.query.filter_by(name=name, category=category).all()
    else:
        charities = Charity.query.filter_by(name=name).all()

    if not charities:
        return jsonify({"error": "No charities found"}), 404

    return jsonify([charity.serialize() for charity in charities]), 200


@serach_bp.route('/event', methods=['GET'])  # route is /search/event
def search_event():
    # search by title
    title = request.json.get('title')

    if not title:
        return jsonify({"error": "Missing data"}), 400

    events = Event.query.filter_by(title=title).all()
    if not events:
        return jsonify({"error": "No events found"}), 404

    return jsonify([event.serialize() for event in events]), 200

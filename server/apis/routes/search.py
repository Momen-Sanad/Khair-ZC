from flask import Blueprint, request, jsonify
from models.dbSchema import Charity, Campaign
from Security import session_required
from models.Notifications import ErrorProcessor

search_bp = Blueprint('search', __name__)
Notifications = ErrorProcessor()

@search_bp.route('/charity', methods=['GET'])  # route is /search/charity
@session_required
def search_charity():
    # Search by name and optionally filter by category
    name = request.args.get('name', '').strip().lower()
    category = request.args.get('category', '').strip()

    if not name:
        return jsonify(Notifications.process_error("search_invalid_name")), 400

    # Add regex for partial search
    regex_name = f"%{name}%"

    # Query charities with optional category filtering
    charities = Charity.query.filter(Charity.name.ilike(regex_name))
    if category:
        charities = charities.filter(Charity.category == category)

    charities = charities.all()

    if not charities:
        return jsonify(Notifications.process_error("search_no_results")), 404

    # Serialize charities into JSON
    json_charities = [
        {
            "id": charity.id,
            "name": charity.name,
            "address": charity.address,
            "description": charity.description,
            "category": charity.category
        } for charity in charities
    ]

    return jsonify(json_charities), 200

@search_bp.route('/campaign', methods=['GET'])  # route is /search/campaign
@session_required
def search_campaign():
    # Search by title
    title = request.args.get('title', '').strip()

    if not title:
        return jsonify(Notifications.process_error("search_invalid_title")), 400

    # Add regex for partial match
    regex_title = f"%{title}%"

    campaigns = Campaign.query.filter(Campaign.title.ilike(regex_title)).all()

    if not campaigns:
        return jsonify(Notifications.process_error("search_no_results")), 404

    # Serialize campaigns into JSON
    json_campaigns = [
        {
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "date": campaign.date,
            "reward": campaign.reward,
            "charity_id": campaign.charity_id,
            "capacity": campaign.capacity
        } for campaign in campaigns
    ]

    return jsonify(json_campaigns), 200

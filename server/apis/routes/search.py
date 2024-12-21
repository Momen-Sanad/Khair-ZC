from flask import Blueprint, request, jsonify
from models.dbSchema import Charity, Campaign
from apis.routes.Security import session_required
from models.Notifications import ErrorProcessor

search_bp = Blueprint('search', __name__)
Notifications = ErrorProcessor()

'''@search_bp.route('/charity', methods=['GET'])
def search_charity():
    name = request.args.get('name', '').strip().lower()
    category = request.args.get('category', '').strip()

    if not name:
        return jsonify(Notifications.process_error("search_invalid_name")), 400

    regex_name = f"%{name}%"

    # Query charities with optional category filtering
    charities = Charity.query.filter(Charity.name.ilike(regex_name))
    if category:
        charities = charities.filter(Charity.category == category)

    charities = charities.all()

    if not charities:
        return jsonify(Notifications.process_error("search_no_results")), 404
    
    # Return search results
    return jsonify([charity.to_dict() for charity in charities])'''


@search_bp.route('/charities', methods=['GET'])
def get_charties():
    charities = Charity.query.all()
    json_charities = [
        {
            "id": charity.id,
            "name": charity.name,
            "address": charity.address,
            "description": charity.description,
            "category": charity.category,
            "image":charity.image
        } for charity in charities
    ]

    return jsonify(json_charities), 200


@search_bp.route('/charities/<int:charity_id>', methods=['GET'])
def get_charity(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    if charity:
        return jsonify({
            "id": charity.id,
            "name": charity.name,
            "address": charity.address,
            "description": charity.description,
            "category": charity.category,
            "image":charity.image
        }), 200

    return jsonify({"error": "Charity not found"}), 404


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
        "date": campaign.date.isoformat(),
        "reward": campaign.reward,
        "charity_id": campaign.charity_id,
        "capacity": campaign.capacity,
        "author": campaign.author,
        "image": campaign.image
    }
    for campaign in campaigns
    ]

    return jsonify(json_campaigns), 200

@search_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.all()
    json_campaigns = [
        {
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "date": campaign.date.isoformat(),
            "reward": campaign.reward,
            "charity_id": campaign.charity_id,
            "capacity": campaign.capacity,
            "author":campaign.author,
            "image":campaign.image
        }
        for campaign in campaigns
    ]
    return jsonify(json_campaigns), 200

@search_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    if campaign:
        return jsonify({
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "date": campaign.date.isoformat(),
            "reward": campaign.reward,
            "charity_id": campaign.charity_id,
            "capacity": campaign.capacity,
            "author":campaign.author,
            "image":campaign.image
        }), 200

    return jsonify({"error": "Campaign not found"}), 404


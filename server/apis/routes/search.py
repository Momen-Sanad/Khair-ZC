from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity, campaign


<<<<<<< HEAD
                    #################################################################################
                    #   TO IMPLEMENT: STRING MATCHING OF USER INPUT AND CURRENT NAMES IN DB         #
                    #   SHOW ALL NAMES BASED ON THEIR STRING MATCHING SCORES IN DESCENDING ORDER    #
                    #   PRIORITY : LOW                                                              #
                    #################################################################################

serach_bp = Blueprint('search', __name__)
=======
serach_bp = Blueprint('search', _name_)
>>>>>>> remotes/origin/backend

# two search endpoints, one for charities and one for campaigns


@serach_bp.route('/charity', methods=['GET'])  # route is /search/charity
def search_charity():
    # search by name and filter by category (optional)
    name = request.json.get('name')
    name = name.lower()
    category = request.json.get('category')
    charities = []



    # add regex for partial search
    # a regex pattern that matches any string that contains the name
    
    regex_name = f"%{name}%"
    regex_name = regex_name.lower()

    # Perform the query with the possibility of filtering by category as well
    if category:
        # Partial match for name and filter by category
        charities = Charity.query.filter(
            Charity.name.like(regex_name), Charity.category == category
        ).all()
    else:
        # Partial match for name only
        charities = Charity.query.filter(Charity.name.like(regex_name)).all()

    # Return an error if no charities are found
    if not charities:
        return jsonify({"error": "No charities found"}), 404

    # serialize charity and return as json object, no attribute serialize in dbSchema
    json_charities = []
    for charity in charities:
        charity = {
            "id": charity.id,
            "name": charity.name,
            "address": charity.address,
            "description": charity.description,
            "category": charity.category
        }
        json_charities.append(charity)

    return jsonify(json_charities), 200


@serach_bp.route('/campaign', methods=['GET'])  # route is /search/campaign
def search_campaign():
    # search by title
    title = request.json.get('title')
    campaigns = []

    if not title:
        return jsonify({"error": "Missing data"}), 400

    regex_title = f"%{title}%"
    campaigns = campaign.query.filter(campaign.title.like(regex_title)).all()
    if not campaigns:
        return jsonify({"error": "No campaigns found"}), 404

    json_campaigns = []
    for campaign in campaigns:
        campaign = {
            "id": campaign.id,
            "title": campaign.title,
            "description": campaign.description,
            "date": campaign.date,
            "reward": campaign.reward,
            "charity_id": campaign.charity_id,
            "capacity": campaign.capacity
        }
        json_campaigns.append(campaign)

    return jsonify(json_campaigns), 200
from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity, Event


                    #################################################################################
                    #   TO IMPLEMENT: STRING MATCHING OF USER INPUT AND CURRENT NAMES IN DB         #
                    #   SHOW ALL NAMES BASED ON THEIR STRING MATCHING SCORES IN DESCENDING ORDER    #
                    #   PRIORITY : LOW                                                              #
                    #################################################################################

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

    # add regex for partial search
    # a regex pattern that matches any string that contains the name
    regex_name = f"%{name}%"

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


@serach_bp.route('/event', methods=['GET'])  # route is /search/event
def search_event():
    # search by title
    title = request.json.get('title')
    events = []

    if not title:
        return jsonify({"error": "Missing data"}), 400

    regex_title = f"%{title}%"
    events = Event.query.filter(Event.title.like(regex_title)).all()
    if not events:
        return jsonify({"error": "No events found"}), 404

    json_events = []
    for event in events:
        event = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "reward": event.reward,
            "charity_id": event.charity_id,
            "capacity": event.capacity
        }
        json_events.append(event)

    return jsonify(json_events), 200

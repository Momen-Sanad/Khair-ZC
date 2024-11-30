import datetime
from flask import Blueprint, request, jsonify, redirect, url_for, session
from requests_oauthlib import OAuth2Session
import oauthlib
import oauth
from flask_bcrypt import Bcrypt
import regex
from functools import wraps
import cryptography
import jwt
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session
from models.dbSchema import db, Event, Charity

event_bp = Blueprint('event', __name__)


@event_bp.route('/create', methods=['POST'])
def create():
    events = request.json  # Expecting a list of events in the request body

    if not events or not isinstance(events, list):
        return jsonify({"error": "Invalid input, expected a list of events"}), 400

    created_events = []
    for event_data in events:
        event_id = event_data.get('eventId')
        event_name = event_data.get('eventName')
        event_reward = event_data.get('eventRe')
        event_desc = event_data.get('eventDesc')
        event_date = event_data.get('eventDate')
        event_cap = event_data.get('eventCap')
        connected_charity = event_data.get('charId')

        # Validate required fields
        if not all([event_name, event_reward, event_desc, event_cap, connected_charity]):
            return jsonify({"error": "Missing required fields for one or more events"}), 400

        # Check if event already exists
        existing_event = Event.query.filter_by(title=event_name).first()
        if existing_event:
            return jsonify({"error": f"Event '{event_name}' already exists"}), 400

        # Check if charity exists
        if not Charity.query.filter_by(id=connected_charity).first():
            return jsonify({"error": f"Charity ID {connected_charity} not found"}), 400

        # Create new event
        new_event = Event(
            id=event_id,
            title=event_name,
            reward=event_reward,
            description=event_desc,
            charity_id=connected_charity,
            date=event_date,
            capacity=event_cap
        )

        db.session.add(new_event)
        created_events.append({"eventId": event_id, "eventName": event_name})

    db.session.commit()
    return jsonify({"message": "Events created successfully", "events": created_events}), 201

    # event_id = request.json.get('eventId')
    # event_name = request.json.get('eventName')
    # event_reward = request.json.get('eventRe')
    # event_desc = request.json.get('eventDesc')
    # event_date = request.json.get('eventDate')
    # event_cap = request.json.get('eventCap')

    # connected_charity = request.json.get('charId')
    # if not all(key in request.json for key in ['eventName', 'eventRe', 'eventDesc', 'eventCap', 'charId']):
    #     return jsonify({"error": "Missing required fields"}), 400
    # if not event_id or not event_name  or not event_reward   or not event_desc  :
    #     return jsonify({"error": "Missing data"}), 400
    # existing_event = Event.query.filter_by(title=event_name).first()
    # if existing_event:
    #     return jsonify({"error": "The event is already found"}), 400

    # if not Charity.query.filter_by(id = connected_charity).first():
    #     return jsonify({
    #         "error" : "You need at least a charity_id to create the event"
    #     }),400

    # # Create a new user instance

    # new_event = Event(id = event_id, title = event_name , reward = event_reward, description = event_desc , charity_id = connected_charity , date = event_date , capacity = event_cap)

    # # Add the user to the session
    # db.session.add(new_event)
    # db.session.commit()
    # return jsonify({"message": "Event created successfully"}), 201

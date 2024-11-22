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

event_bp = Blueprint('event', __name__)


@event_bp.route('/create' , methods=['POST'])
def create():
    from models.dbSchema import db,Event,Charity
    event_id = request.json.get('eventId')
    event_name = request.json.get('eventName')
    event_reward = request.json.get('eventRe')
    event_desc = request.json.get('eventDesc')
    event_date = request.json.get('eventDate')
    
    connected_charity = request.json.get('charId')

    if not event_id or not event_name  or not event_reward   or not event_desc  :
        return jsonify({"error": "Missing data"}), 400
    existing_event = Event.query.filter_by(title=event_name).first()
    if existing_event:
        return jsonify({"error": "The event is already found"}), 400

    if not Charity.query.filter_by(id = connected_charity).first():
        return jsonify({
            "error" : "You need at least a charity_id to create the event"
        }),400
    
    
    # Create a new user instance

    new_event = Event(id = event_id, title = event_name , reward = event_reward, description = event_desc , charity_id = connected_charity , date = event_date )

    # Add the user to the session
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully"}), 201
    
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
from models.dbSchema import db, Charity

charity_bp = Blueprint('charity', __name__)


@charity_bp.route('/create', methods=['POST'])
def create():

    #admin checker
    user_id = request.json.get('userId')  

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # retrieve the user from the database
    user = User.query.filter_by(id=user_id).first()
    if not user or not user.is_admin:
        return jsonify({"error": "Only admins can create charities"}), 403


    # Create a new charity    from models.dbSchema import db,User
    charities = request.json  # Expecting a list of charities in the request body

    if not charities or not isinstance(charities, list):
        return jsonify({"error": "Invalid input, expected a list of charities"}), 400

    created_charities = []
    for charity_data in charities:

        charity_id = charity_data.get('charId')
        charity_name = charity_data.get('charName')
        charity_address = charity_data.get('charAdd')
        charity_desc = charity_data.get('charDesc')
        charity_cat = charity_data.get('charCat')

        # Validate required fields
        if not all([charity_name, charity_address, charity_desc, charity_cat]):
            return jsonify({"error": "Missing required fields for one or more charities"}), 400

        # Check if charity already exists
        existing_charity = Charity.query.filter_by(name=charity_name).first()
        if existing_charity:
            return jsonify({"error": f"Charity '{charity_name}' already exists"}), 400

        # Create new charity
        new_charity = Charity(
            id=charity_id,
            name=charity_name,
            address=charity_address,
            description=charity_desc,
            category=charity_cat
        )

        db.session.add(new_charity)
        created_charities.append(
            {"charityId": charity_id, "charityName": charity_name})

    db.session.commit()
    return jsonify({"message": "Charities created successfully", "charities": created_charities}), 201

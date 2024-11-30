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

charity_bp = Blueprint('charity', __name__)


@charity_bp.route('/create' , methods=['POST'])
def create():
    # Create a new charity    from models.dbSchema import db,User
    from models.dbSchema import db,Charity
    charity_id = request.json.get('charId')
    charity_name = request.json.get('charName')
    charity_address = request.json.get('charAdd')
    charity_desc = request.json.get('charDesc')
    charity_cat = request.json.get('charCat')

    if not charity_id or not charity_name  or not charity_address or not charity_desc or not charity_cat  :
        return jsonify({"error": "Missing data"}), 400
    existing_user = Charity.query.filter_by(name=charity_name).first()
    if existing_user:
        return jsonify({"error": "The charity is already found"}), 400

    # Create a new user instance

    new_charity = Charity(id = charity_id, name = charity_name , address = charity_address,  description = charity_desc, category = charity_cat)

    # Add the user to the session
    db.session.add(new_charity)
    db.session.commit()
    return jsonify({"message": "Charity created successfully"}), 201
    
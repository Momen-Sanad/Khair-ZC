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
from apis.routes.Security import session_required, admin_required
from models.Notifications import ErrorProcessor
points_bp = Blueprint('points', __name__)

@points_bp.route('/create' , methods=['POST'])
def points():
    from models.dbSchema import db
    pass

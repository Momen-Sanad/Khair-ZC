from datetime import timedelta, datetime
from flask import Blueprint, request, jsonify, session, current_app
from requests_oauthlib import OAuth2Session
from flask_bcrypt import Bcrypt
import regex
from functools import wraps
import jwt
import uuid  # for auto-generating unique IDs
from models.Notifications import ErrorProcessor
from apis.routes.Security import session_required, check_session_timeout
from models.dbSchema import db, User

# Initialize blueprint and utilities
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
Notifications = ErrorProcessor()

# session expiration
@auth_bp.before_app_request
def register_session_timeout():
    response = check_session_timeout()
    if response:
        return response

def token_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return Notifications.process_error("login_invalid"), 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify(Notifications.process_error("login_invalid")), 403
        return f(current_user, *args, **kwargs)

    return decorated_function

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():

    user_id = str(uuid.uuid4())  # auto-generated user ID

    first_name = request.json.get('fname')
    last_name = request.json.get('lname')
    password = request.json.get('userPass')
    email = request.json.get('email')

    if not first_name or not last_name or not password or not email:
        return jsonify(Notifications.process_error("signup_invalid_password")), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(Notifications.process_error("signup_invalid_email")), 400

    # Create a new user instance
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(id=user_id, fname=first_name, lname=last_name, password=hashed_password, email=email)

    # Pattern for Zewailian email validation
    pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'

    if regex.match(pattern, email):
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Notifications.process_error("signup_success")), 201
    else:
        return jsonify({"message": "User Entered as a Guest", "status": "success"}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('userPass')
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify(Notifications.process_error("login_invalid")), 404

    # Check if the provided password matches the stored hash
    if bcrypt.check_password_hash(user.password, password):
        # Create a JWT token
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
            current_app.config['SECRET_KEY'],  # Your secret key for encoding
            algorithm="HS256"  # The algorithm to use
        )

        # Set session values
        session['logged_in'] = True
        session['user_id'] = user.id  # Optionally store the user ID in the session
        session['last_activity'] = datetime.utcnow().isoformat()  # Track activity for timeout

        return jsonify(Notifications.process_error("login_success"), token=token), 200
    else:
        return jsonify(Notifications.process_error("login_invalid")), 401

# Logout route
@auth_bp.route('/logout', methods=['POST'])
@session_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)  # Clear the user ID from the session
    session.pop('last_activity', None)  # Clear the last activity timestamp
    return jsonify({
        "message": "Logged out successfully!",
        "notification": "You have been logged out."
    })

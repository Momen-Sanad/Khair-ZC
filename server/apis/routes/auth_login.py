import random
import string
from models.Notifications import ErrorProcessor
from models.dbSchema import db, User
from apis.routes.Security import session_required, check_session_timeout
from datetime import datetime ,timedelta
from flask import Blueprint, redirect, request, jsonify, session
from requests_oauthlib import OAuth2Session
from flask_bcrypt import Bcrypt
import regex
from functools import wraps
import jwt
import uuid  # for auto-generating unique IDs
import requests
import os


# Initialize blueprint and utilities
auth_bp = Blueprint('auth', __name__)
oauth_bp = Blueprint('oauth',__name__)
bcrypt = Bcrypt()
Notifications = ErrorProcessor()


# session expiration
@auth_bp.before_app_request
def register_session_timeout():
    response = check_session_timeout()
    if isinstance(response, dict):
        return jsonify(response)
    return response


def token_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(Notifications.process_error("login_invalid")), 403
        try:
            data = jwt.decode(
                token, auth_bp.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify(Notifications.process_error("login_invalid")), 403
        return f(current_user, *args, **kwargs)

    return decorated_function


#some helper functions
def clear_session():
    """Clears all session data securely."""
    session_keys = ['logged_in', 'user_id', 'last_activity', 'email', 'state', 'access_token']
    for key in session_keys:
        session.pop(key, None)


def generate_token(user_id, expiration_hours=24):
    """Generates a JWT for the user."""
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        },
        os.environ.get('SECRET_KEY', 'your_secret_key'),  # Securely fetch the secret key
        algorithm="HS256"
    )


#first route
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

    PasswordRegex = r'^(?=(.*[a-zA-Z]))(?=(.*\d))(?=.{7,})'
    if not regex.match(PasswordRegex, password):
        return jsonify(Notifications.process_error("signup_invalid_password")), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(id=user_id, fname=first_name, lname=last_name,
                    password=hashed_password, email=email)

    # Add the user to the session
    db.session.add(new_user)
    db.session.commit()

    # Pattern for Zewailian email validation
    pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'

    if regex.match(pattern, email):
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Notifications.process_error("signup_success")), 201
    else:
        return jsonify({"message": "User Entered as a Guest", "status": "success"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('userPass')

        if not email or not password:
            return jsonify(Notifications.process_error("login_invalid_fields")), 400

        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify(Notifications.process_error("login_invalid")), 404

        # Check password validity
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify(Notifications.process_error("login_invalid")), 401

        # Generate token
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24),
            },
            os.environ.get('SECRET_KEY', 'your_secret_key'),  # Use an environment variable
            algorithm="HS256"
        )

        # Set session data securely
        session['logged_in'] = True
        session['user_id'] = user.id
        session['last_activity'] = datetime.utcnow().isoformat()

        response_data = Notifications.process_error("login_success")
        response_data['token'] = token

        return jsonify(response_data), 200

    except Exception as e:
        # Log unexpected errors
        app.logger.error(f"Error during login: {str(e)}")
        return jsonify({"message": "An error occurred during login.", "status": "error"}), 500


@oauth_bp.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    state = request.args.get('state')
    code = request.args.get('code')

    if state != session.get('state'):
        return "Invalid state parameter! Possible CSRF attack.", 400

    # Exchange the authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': os.environ.get('CLIENT_ID'),  # OAuth client ID
        'client_secret': os.environ.get('CLIENT_SECRET'),  # OAuth client secret
        'redirect_uri': 'http://localhost:5000/oauth/oauth2callback',  # Redirect URI
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    token_info = response.json()

    if 'access_token' in token_info:
        session['access_token'] = token_info['access_token']
        user_info = get_google_user_info()  # Fetch user info from Google

        # If there was an issue fetching user info, return an error
        if isinstance(user_info, str):  
            return jsonify({'message': user_info}), 400

        # Check if the user already exists in your database using their email
        user = User.query.filter_by(email=user_info['email']).first()

        if not user:
            # If user doesn't exist, register them using data from Google
            user_id = str(uuid.uuid4())  # Optionally generate a unique user ID
            hashed_password = bcrypt.generate_password_hash("defaultpassword").decode('utf-8')  # Set a default password or let them change it later

            # Create a new user with Google data
            new_user = User(
                id=user_id,
                fname=user_info['given_name'],  # Assuming 'given_name' from Google
                lname=user_info['family_name'],  # Assuming 'family_name' from Google
                email=user_info['email'],
                password=hashed_password
            )

            pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'

            if regex.match(pattern,user_info['email']):
                db.session.add(new_user)
                db.session.commit()

            # Generate JWT token
            token = jwt.encode(
                {'user_id': new_user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
                'your_secret_key',  # Your secret key for encoding
                algorithm="HS256"  # The algorithm to use
            )

            # Set session values
            session['logged_in'] = True
            session['user_id'] = new_user.id
            session['last_activity'] = datetime.utcnow().isoformat()

            response_data = Notifications.process_error("login_success")
            response_data['token'] = token  # Add the JWT token to the response

            return jsonify({
                'message': 'Login successful via OAuth, user created!',
                'token': token  # Include the JWT token in the response
            }), 200

        else:
            # If the user exists, log them in and generate JWT token
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
                'your_secret_key',  # Your secret key for encoding
                algorithm="HS256"  # The algorithm to use
            )

            # Set session values
            session['logged_in'] = True
            session['user_id'] = user.id
            session['last_activity'] = datetime.utcnow().isoformat()

            return jsonify({
                'message': 'Login successful via OAuth',
                'token': token  # Include the JWT token in the response
            }), 200

    else:
        return "Failed to get access token!", 400
    
    
    
    
def get_google_user_info():
    access_token = session.get('access_token')
    if not access_token:
        return "Access token is missing.", 403

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the user's profile info
    else:
        return "Failed to fetch user info", 400

def generate_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@oauth_bp.route('/login' , methods = ['GET'])
def login():
    state = generate_state()
    session['state'] = state  # Save the state to the session
    client_id = os.environ.get('CLIENT_ID')
    redirect_uri = 'http://localhost:5000/oauth/oauth2callback'
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=email%20profile"
        f"&state={state}"
    )
    return redirect(auth_url)
from flask import make_response


@auth_bp.route('/logout', methods=['POST'])
@session_required
def logout():
    try:
        # Clear session data
        clear_session()

        # Prepare response with cookie clearing
        response = make_response(jsonify({
            "message": "Logged out successfully!",
            "notification": "You have been logged out."
        }))
        response.delete_cookie('session')  # Delete the session cookie
        response.delete_cookie('csrf_token', path='/')  # Delete CSRF token cookie if applicable

        return response

    except Exception as e:
        # Log unexpected errors
        app.logger.error(f"Error during logout: {str(e)}")
        return jsonify({"message": "An error occurred during logout.", "status": "error"}), 500

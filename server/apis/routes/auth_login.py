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
import uuid         #   for auto generating unique IDs


auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
def token_required(f):
    from models.dbSchema import db,User
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, auth_bp.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    from models.dbSchema import db,User
    
    userId = str(uuid.uuid4())          #auto generated user id

    firstName = request.json.get('fname')
    lastName = request.json.get('lname')
    password = request.json.get('userPass')
    email = request.json.get('email')

    if not firstName or not lastName  or not password or not email:
        return jsonify({"error": "Missing data"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Create a new user instance
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(id = userId,fname = firstName , lname = lastName , password=hashed_password, email=email )

    # Add the user to the session
    db.session.add(new_user)
    db.session.commit()
    
    pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'           # s-aefaef.awdaw@zewailcity.edu.eg
                                                                        # ^^______^_____^^^^^^^^^^^^^^^^^^

# Check if the email matches the pattern
    if regex.match(pattern, email):
        return jsonify({"message": "User Registered as Zewailian"}), 201

    else:
        return jsonify({"message" :"User Registered as a Guest"}) , 201
    
@auth_bp.route('/login', methods=['POST'])
def login():

   
    from models.dbSchema import db,User
    email = request.json.get('email')
    password = request.json.get('userPass')
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "User not found!"}), 404

    # Check if the provided password matches the stored hash
    if bcrypt.check_password_hash(user.password, password):
        # Password is correct
        token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        'your_secret_key',  # Your secret key for encoding
        algorithm="HS256"   # The algorithm to use
        )

        return jsonify({"message": "Login successful!" , 'token': token}), 200
    
    else:
        # Password is incorrect
        return jsonify({"error": "Invalid credentials!" ,'token': token}), 401
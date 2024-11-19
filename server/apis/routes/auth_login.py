from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
import cryptography
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    from models.dbSchema import db,User

    userId = request.json.get('id')
    firstName = request.json.get('fname')
    lastName = request.json.get('lname')
    password = request.json.get('userPass')
    email = request.json.get('email')

    if not firstName or not lastName  or not password or not email or not userId  :
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

    return jsonify({"message": "User successfully added!"}), 201
    
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
        return jsonify({"message": "Login successful!"}), 200
    else:
        # Password is incorrect
        return jsonify({"error": "Invalid credentials!"}), 401



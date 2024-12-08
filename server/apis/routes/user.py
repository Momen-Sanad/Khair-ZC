from flask import Blueprint, request, jsonify, redirect, url_for, session
from models.dbSchema import db, Charity, User
# this is for hashing passwords
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/create', methods=['POST'])
def create_user():
    user_id = request.json.get  ('user_id')
    password = request.json.get('password')
    fname = request.json.get      ('fname')
    lname = request.json.get      ('lname')
    email = request.json.get      ('email')
    points = request.json.get    ('points')
    is_admin = request.json.get   ('admin')     #boolean
    
    # Check if user already exists
    if db.session.query(User).filter(User.id == user_id).first():
        return jsonify({'message': 'User already exists'}), 400

    # Hash password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(id=user_id, password=hashed_password,
                    fname=fname, lname=lname, email=email, points=points)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

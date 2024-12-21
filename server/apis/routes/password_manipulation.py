from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import regex
from models.dbSchema import db, User
from models.Notifications import ErrorProcessor

password_bp = Blueprint('password', __name__)
bcrypt = Bcrypt()
Notifications = ErrorProcessor()


# Validation Service
class PasswordValidator:
    @staticmethod
    def validate(password):
        regex_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.{7,})'
        return bool(regex.match(regex_pattern, password))


class EmailValidator:
    @staticmethod
    def validate(email):
        pattern = r'^s-[a-zA-Z]+\.[a-zA-Z]+@zewailcity\.edu\.eg$'
        return bool(pattern in email)  


# User Service (Handles User Logic)
class UserService:
    @staticmethod
    def find_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def update_password(user, new_password):
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()


# Endpoints
@password_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    if not email or not EmailValidator.validate(email):
        return jsonify(Notifications.process_error("email_missing")), 400

    user = UserService.find_user_by_email(email)
    if not user:
        return jsonify(Notifications.process_error("user_not_found")), 404

    reset_token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
        'your_secret_key',
        algorithm="HS256"
    )

    return jsonify({
        "message": "Password reset request sent successfully!",
        "reset_token": reset_token
    }), 200


@password_bp.route('/reset_password', methods=['POST'])
def reset_password():
    reset_token = request.json.get('reset_token')
    new_password = request.json.get('new_password')

    if not reset_token or not new_password or not PasswordValidator.validate(new_password):
        return jsonify(Notifications.process_error("reset_invalid_data")), 400

    try:
        decoded_data = jwt.decode(reset_token, 'your_secret_key', algorithms=["HS256"])
        user = UserService.find_user_by_id(decoded_data['user_id'])

        if not user:
            return jsonify(Notifications.process_error("user_not_found")), 404

        UserService.update_password(user, new_password)
        return jsonify(Notifications.process_error("password_reset_success")), 200

    except jwt.ExpiredSignatureError:
        return jsonify(Notifications.process_error("reset_token_expired")), 401
    except jwt.InvalidTokenError:
        return jsonify(Notifications.process_error("reset_token_invalid")), 401


@password_bp.route('/change_password', methods=['POST'])
@session_required
def change_password():
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')

    if not current_password or not new_password or not PasswordValidator.validate(new_password):
        return jsonify(Notifications.process_error("change_invalid_data")), 400

    # Fetch the user from the session
    user_id = session.get('user_id')
    user = UserService.find_user_by_id(user_id)

    if not bcrypt.check_password_hash(user.password, current_password):
        return jsonify(Notifications.process_error("password_incorrect")), 401

    UserService.update_password(user, new_password)
    return jsonify(Notifications.process_error("password_change_success")), 200
from functools import wraps
from flask import session, jsonify, current_app,Blueprint
from datetime import datetime, timedelta

security_bp = Blueprint('security', __name__)


def check_session_timeout():
    """
    Middleware function to check session timeout.
    Should be registered as a @before_app_request function.
    """
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout set to 30 minutes

    last_activity = session.get('last_activity')
    if last_activity:
        if datetime.utcnow() > datetime.fromisoformat(last_activity) + timedelta(minutes=30):
            session.clear()  # Clear session if timeout exceeded
            return jsonify({"message": "Session expired, please log in again."}), 403
    session['last_activity'] = datetime.utcnow().isoformat()


def session_required(f):
    """
    Decorator to ensure the user is logged in with an active session.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Session debug:", session)  # Add this line
        if not session.get('logged_in'):
            return jsonify({
                "message": "Session is missing or invalid!",
                "notification": "Please log in to access this resource."
            }), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to ensure the user has admin privileges.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in by verifying session data
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                "message": "Unauthorized access!",
                "notification": "You must be logged in to perform this action."
            }), 403

        # Fetch the user from the database
        from models.dbSchema import User  # Ensure you import your database schema
        user = User.query.filter_by(id=user_id).first()

        # Check if the user exists and has admin privileges
        if not user or not getattr(user, 'is_admin', False):
            return jsonify({
                "message": "Access denied!",
                "notification": "You do not have sufficient privileges."
            }), 403

        # Allow access to the route
        return f(*args, **kwargs)
    return decorated_function

from flask import session, jsonify


@security_bp.route('/user', methods=['GET'])
@session_required
def get_user():
    print("Session ID:", session.get('user_id'))  # Add this line
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            "message": "User not found in session.",
            "notification": "Please log in to access your profile."
        }), 404
    
    from models.dbSchema import User
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({
            "message": "User not found.",
            "notification": "No user found with the provided ID."
        }), 404
    
    return jsonify({
        "id": user.id,
        "firstName": user.fname,
        "lastName": user.lname,
        "email": user.email,
        "isAdmin": user.is_admin,
        "points": user.points
    })


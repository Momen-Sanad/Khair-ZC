
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models.dbSchema import db
from apis.routes.auth_login import auth_bp  # Import the auth blueprint

# Initialize the db object
def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Register the blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Prefix routes with /auth

    return app

# Create the app instance
app = create_app()

# Ensure tables are created when the app starts
with app.app_context():
    db.create_all()  # Create all the tables defined in models
    print("Tables created successfully!")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
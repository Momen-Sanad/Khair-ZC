from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dbSchema import db

# Initialize the db object

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import routes to register them

    return app

if __name__ == '__main__':
    app = create_app()
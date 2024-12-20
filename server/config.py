import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

DATABASE_MODE='railway'

class Config:
    # Secret key for session management (required by Flask)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')  # default for development
    
    # Disable track modifications for SQLAlchemy (recommended to improve performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration using environment variables

    DB_USERNAME = urllib.parse.quote(os.getenv('DB_USERNAME', 'root'))
    DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD', 'password'))

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 3306)  # default MySQL port
    DB_NAME = os.getenv('DB_NAME', 'my_database')
    # Print the database URI for debugging
    print(f"Database URI: mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    try:
        # Test the connection with SQLAlchemy engine
        from sqlalchemy import create_engine
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        print("Successfully connected to the database!")
    except Exception as e:
        print(f"Error: {e}")


import os
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

# Mode can be 'local' or 'railway'
DATABASE_MODE = os.getenv('DATABASE_MODE', 'railway')

class Config:
    # Secret key for session management (required by Flask)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')  # default for development
    
    # Disable track modifications for SQLAlchemy (recommended to improve performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    if DATABASE_MODE == 'railway':
        # Railway Database Configuration
        DB_USERNAME = urllib.parse.quote(os.getenv('RAILWAY_DB_USERNAME', 'root'))
        DB_PASSWORD = urllib.parse.quote(os.getenv('RAILWAY_DB_PASSWORD', 'password'))
        DB_HOST = os.getenv('RAILWAY_DB_HOST', 'localhost')
        DB_PORT = os.getenv('RAILWAY_DB_PORT', 3306)
        DB_NAME = os.getenv('RAILWAY_DB_NAME', 'railway')

        print("Using Railway Database")
    else:
        # Local Database Configuration
        DB_USERNAME = urllib.parse.quote(os.getenv('DB_USERNAME', 'root'))
        DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD', 'password'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', 3306)
        DB_NAME = os.getenv('DB_NAME', 'my_database')

        print("Using Local Database")

    # Construct the database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Print the database URI for debugging
    print(f"Database URI: {SQLALCHEMY_DATABASE_URI}")
    
    # Test the connection with SQLAlchemy engine
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        print(f"Successfully connected to the {DATABASE_MODE} database!")
        connection.close()  # Close the connection when done
    except Exception as e:
        print(f"Error: {e}")  # Error message if connection fails

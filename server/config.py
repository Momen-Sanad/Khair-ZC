import os
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy import create_engine

load_dotenv()

# Switch to choose between database configurations
# Possible values: 'local' or 'railway'
DATABASE_MODE = 'local'


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USERNAME = urllib.parse.quote(os.getenv('DB_USERNAME', 'root'))
    DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD', 'password'))
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_NAME = os.getenv('DB_NAME', 'my_database')

    RAILWAY_DB_USERNAME = os.getenv('RAILWAY_DB_USERNAME')
    RAILWAY_DB_PASSWORD = os.getenv('RAILWAY_DB_PASSWORD')
    RAILWAY_DB_HOST = os.getenv('RAILWAY_DB_HOST')
    RAILWAY_DB_PORT = os.getenv('RAILWAY_DB_PORT')
    RAILWAY_DB_NAME = os.getenv('RAILWAY_DB_NAME')

    @classmethod
    def get_database_uri(cls):
        if DATABASE_MODE == 'local':
            username = cls.DB_USERNAME
            password = cls.DB_PASSWORD
            host = cls.DB_HOST
            port = cls.DB_PORT
            db_name = cls.DB_NAME
        elif DATABASE_MODE == 'railway':
            username = urllib.parse.quote(cls.RAILWAY_DB_USERNAME)
            password = urllib.parse.quote(cls.RAILWAY_DB_PASSWORD)
            host = cls.RAILWAY_DB_HOST
            port = cls.RAILWAY_DB_PORT
            db_name = cls.RAILWAY_DB_NAME
        else:
            raise ValueError(
                "Invalid DATABASE_MODE. Choose 'local' or 'railway'")

        print(f"Connecting to database: {username}@{host}:{port}/{db_name}")

        if DATABASE_MODE == 'local':
            return f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'
        elif DATABASE_MODE == 'railway':
            return f'mysql://{username}:{password}@{host}:{port}/{db_name}'


SQLALCHEMY_DATABASE_URI = Config.get_database_uri()

Config.SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

try:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("Successfully connected to the database!")
except Exception as e:
    print(f"Error: {e}")

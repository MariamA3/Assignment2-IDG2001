import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Initialize SQLAlchemy
db = SQLAlchemy()

def get_db_connection(app):
    # Load environment variables from .env file
    load_dotenv()

    # Get database connection details from environment variables
    DB_HOST = os.getenv('MYSQLHOST')
    DB_PORT = os.getenv('MYSQLPORT')  # no need to convert to int for SQLAlchemy
    DB_USER = os.getenv('MYSQLUSER')
    DB_PASSWORD = os.getenv('MYSQLPASSWORD')
    DB_NAME = os.getenv('MYSQLDATABASE')

    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    return db

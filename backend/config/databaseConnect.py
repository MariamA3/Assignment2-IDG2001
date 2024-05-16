import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def get_db_connection(app):
    # Load environment variables from .env file
    load_dotenv()

    # Get database connection details from environment variables
    DB_HOST = os.getenv('MYSQLHOST', 'default_host')  # Provide default values if not set
    DB_PORT = os.getenv('MYSQLPORT', '3306')  # Default MySQL port
    DB_USER = os.getenv('MYSQLUSER', 'root')  # Default user
    DB_PASSWORD = os.getenv('MYSQLPASSWORD', 'password')  # Default password
    DB_NAME = os.getenv('MYSQLDATABASE', 'my_database')  # Default database name

    # Ensure that the port is a valid integer
    try:
        int(DB_PORT)  # This checks if DB_PORT is a valid integer
    except ValueError:
        raise ValueError(f"Invalid port number: {DB_PORT}")

    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with SQLAlchemy, passing the app object
    db.init_app(app)

    # Return the db object, which can be used to interact with the database
    return db

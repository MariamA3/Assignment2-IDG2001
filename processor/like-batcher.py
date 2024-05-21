import time
import redis
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

# Initialize Flask app and load environment variables
app = Flask(__name__)
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Gotta fix this somehow, when try to import database, it doesnt work, so having db 
#connection here is the only way it works for some reason.

# Set up database connection
def setup_db_connection(app):
    # Get database connection details from environment variables
    DB_HOST = os.getenv('MYSQLHOST', 'roundhouse.proxy.rlwy.net')
    DB_PORT = int(os.getenv('MYSQLPORT', 41431))
    DB_USER = os.getenv('MYSQLUSER', 'root')
    DB_PASSWORD = os.getenv('MYSQLPASSWORD', 'QTEYjOFgnGrzSBJmjwOSKxONEorguzdn')
    DB_NAME = os.getenv('MYSQLDATABASE', 'railway')

    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with SQLAlchemy
    db.init_app(app)

setup_db_connection(app)

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')  # Change 'localhost' to 'redis' if running in Docker
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Function to process likes
def process_likes():
    while True:
        # Check Redis for pending likes
        pending_likes = redis_client.lrange('pending_likes', 0, -1)
        if pending_likes:
            # Process likes in batches
            #sends after 11 likes has been registered
            batch_size = 10
            for i in range(0, len(pending_likes), batch_size):
                batch = pending_likes[i:i+batch_size]
                process_likes_batch(batch)

            # Remove processed likes from Redis
            redis_client.ltrim('pending_likes', len(pending_likes), -1)

        # Wait for some time before checking again
        time.sleep(60)

# Function to process each batch of likes
def process_likes_batch(batch):
    # Example: Update database with likes
    with app.app_context():
        for like in batch:
            process_like(json.loads(like))

# Function to process individual like
def process_like(like):
    with app.app_context():
        try:
            # Example: Insert like into database
            sql = text("INSERT INTO likes (user_id, post_id) VALUES (:user_id, :post_id)")
            db.session.execute(sql, {'user_id': like['user_id'], 'post_id': like['post_id']})
            db.session.commit()
            print("Like inserted successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error inserting like into the database: {e}")

if __name__ == '__main__':
    process_likes()

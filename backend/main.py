from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from redis_cache import RedisCache
import os
import redis
import json

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Manually set configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Initialize extensions with the app
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
redis_cache = RedisCache()

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'), 
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

# Import database connection and models after config is set
from config.databaseConnect import get_db_connection, db
from routes.users import users
from routes.posts import posts
from routes.categories import categories

# Establish a database connection when the application starts
get_db_connection(app)

# Print a message to the console to confirm the connection
print("Connected to the database!")

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)

# Define a route for the root URL
@app.route('/like', methods=['POST'])
def like_post():
    data = request.json
    if 'user_id' not in data or 'post_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Enqueue the like in Redis
    redis_client.rpush('pending_likes', json.dumps(data))
    return jsonify({'status': 'Like enqueued'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

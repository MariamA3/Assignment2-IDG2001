from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
# Legger denne inn for å importere redis modulen, her kan man legge inn 
from redis_cache import RedisCache
import os

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)

# Manually set configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Example additional configuration

# Initialize extensions with the app
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Initialize RedisCache instance ----
redis_cache = RedisCache()

# Import database connection and models after config is set
from config.databaseConnect import get_db_connection, db
from routes.users import users
from routes.posts import posts
from routes.categories import categories

# Establish a database connection when the application starts
get_db_connection(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)

# Define a route for the root URL
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

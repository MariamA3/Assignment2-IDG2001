from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
CORS(app, origins=["http://129.114.25.110:8080"], supports_credentials=True)

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

# Import database connection and models after config is set
from config.databaseConnect import get_db_connection, db
from routes.users import users
from routes.posts import posts
from routes.categories import categories
from routes.likes import likes  # Import the new likes blueprint

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
app.register_blueprint(likes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

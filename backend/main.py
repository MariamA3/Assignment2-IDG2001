# Imports
from flask import Flask
from routes.users import users
from routes.posts import posts
from routes.categories import categories
from config.databaseConnect import get_db_connection

app = Flask(__name__)

# Establish a database connection when the application starts
db_connection = get_db_connection()

if db_connection:
    # Store the database connection in app.config for access in routes
    app.config['DB_CONNECTION'] = db_connection
else:
    # Handle database connection failure gracefully
    print("Database connection failed. Exiting...")
    exit(1)

# Registering the blueprints (routes aka endpoints)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
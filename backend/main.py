# Imports
from flask import Flask
# Importing routes aka endpoints
from routes.users import users
from routes.posts import posts
from routes.categories import categories

# Creating the Flask app
app = Flask(__name__)
# Registering the blueprints (routes aka endpoints)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)

# Running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
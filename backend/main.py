from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from routes.users import users
from routes.posts import posts
from routes.categories import categories
from config.databaseConnect import get_db_connection, db

app = Flask(__name__)
app.config.from_pyfile('.env')

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Establish a database connection when the application starts
get_db_connection(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Registering the blueprints (routes aka endpoints)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

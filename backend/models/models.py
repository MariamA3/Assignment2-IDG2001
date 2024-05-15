# Description: This file contains the models for the database tables.
# A model represents a table in the database and is used to interact with the data in that table.
# In this file, we define three models: User, Post, and Category.

# Import the db object from the databaseConnect module
from config.databaseConnect import db

# Define the User model, which represents the users table in the database
# The User model has three columns: user_id, username, email, and password, which correspond to the columns in the users table
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Define the Post model, which represents the posts table in the database
# The Post model has four columns: post_id, title, content, user_id, and category_id, which correspond to the columns in the posts table
class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

# Define the Category model, which represents the categories table in the database
# The Category model has two columns: category_id and name, which correspond to the columns in the categories table
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

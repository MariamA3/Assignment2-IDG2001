# Description: This file contains the models for the database tables.
# A model represents a table in the database and is used to interact with the data in that table.
# In this file, we define four models: User, Post, category and likes.

# Import the db object from the databaseConnect module
from config.databaseConnect import db

# Import the datetime module
from datetime import datetime

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user= db.relationship('User', backref=db.backref('posts', lazy=True))
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))


# Define the Category model, which represents the categories table in the database
# The Category model has two columns: category_id and name, which correspond to the columns in the categories table
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)


#Define the Likes model, which represents the likes table in the database
# The Likes model has four columns: like_id, user_id, post_id, and created_at, which correspond to the columns in the likes table
class Likes(db.Model):
    __tablename__ = 'likes'
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define relationships
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Post', backref=db.backref('likes', lazy=True))

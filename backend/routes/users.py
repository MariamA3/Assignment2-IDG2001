from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from config.databaseConnect import db
from models.models import User
from schemas.schemas import UserCreate, UserLogin
from utils import hash_password, verify_password

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_data = UserCreate(**data)
    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username or email already exists"}), 400

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = UserLogin(**data)
    user = User.query.filter_by(username=user_data.username).first()
    if user and verify_password(user_data.password, user.password):
        access_token = create_access_token(identity=user.username)
        # Create a response
        response = make_response(jsonify({"msg": "Login successful"}), 200)

        # Set the access_token as a cookie in the response
        response.set_cookie('access_token', access_token)

        return response
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@users.route('/profile', methods=['GET'])
@jwt_required()
def profile():
   current_user = get_jwt_identity()
   user = User.query.filter_by(username=current_user).first_or_404()
   return jsonify(username=user.username), 200

@users.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
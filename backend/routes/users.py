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

from flask_jwt_extended import set_access_cookies, create_access_token

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = UserLogin(**data)
    user = User.query.filter_by(username=user_data.username).first()
    if user and verify_password(user_data.password, user.password):
        access_token = create_access_token(identity=user.username)
        # Create a response
        response = make_response(jsonify({"msg": "Login successful"}), 200)

        # Set the JWT cookies in the response
        set_access_cookies(response, access_token)

        return response
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@users.route('/profile', methods=['GET'])
@jwt_required()
def profile():
   current_user = get_jwt_identity()
   user = User.query.filter_by(username=current_user).first_or_404()
   return jsonify(username=user.username, email=user.email, user_id=user.user_id), 200

@users.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = make_response(jsonify({"message": "Logged out successfully"}))
    resp.set_cookie('access_token', '', expires=0)
    resp.set_cookie('csrf_access_token', '', expires=0)
    return resp, 200

@users.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(username=user.username, email=user.email, user_id=user.user_id), 200

# GET a specific user by username
@users.route('/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(username=user.username, email=user.email, user_id=user.user_id), 200

# DELETE a user by username
@users.route('/users/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify({"message": "Cannot delete other user's account"}), 403

    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

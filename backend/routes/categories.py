from flask import Blueprint, request, jsonify
from config.databaseConnect import db
from models.models import Category
from redis_cache import RedisCache
import json
import redis
import logging

# Create a Blueprint object for categories, with the /api prefix
categories = Blueprint('categories', __name__, url_prefix='/api')

# Initialize RedisCache instance
redis_cache = RedisCache()

# Helper function to serialize SQLAlchemy objects
def serialize_category(category):
    return {
        'category_id': category.category_id,
        'name': category.name
    }

# GET all categories, returns a list of all categories
@categories.route('/categories', methods=['GET'])
def get_categories():
    try:
        # Check if categories are cached
        categories_data = redis_cache.get_data('categories')
        if not categories_data:
            print("Categories not found in cache, querying database.")
            categories_data = Category.query.all()
            # Serialize the data before caching
            serialized_data = [serialize_category(category) for category in categories_data]
            # Cache categories data for 1 hour (3600 seconds)
            redis_cache.set_data('categories', serialized_data, expire=3600)
        else:
            print("Categories found in cache.")
            # Deserialize the data from cache
            serialized_data = categories_data
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
        # If Redis is unavailable, fallback to querying the database
        categories_data = Category.query.all()
        serialized_data = [serialize_category(category) for category in categories_data]

    return jsonify(serialized_data)

# GET a specific category by ID, returns the category with the specified ID
@categories.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    try:
        # Check if category data is cached
        category_data = redis_cache.get_data(f'category_{id}')
        if not category_data:
            print(f"Category {id} not found in cache, querying database.")
            category_data = Category.query.get(id)
            if not category_data:
                return jsonify({'message': 'Category not found'}), 404
            # Serialize the data before caching
            serialized_data = serialize_category(category_data)
            # Cache category data for 1 hour (3600 seconds)
            redis_cache.set_data(f'category_{id}', serialized_data, expire=3600)
        else:
            print(f"Category {id} found in cache.")
            # Deserialize the data from cache
            serialized_data = category_data
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
        # If Redis is unavailable, fallback to querying the database
        category_data = Category.query.get(id)
        if not category_data:
            return jsonify({'message': 'Category not found'}), 404
        serialized_data = serialize_category(category_data)

    return jsonify(serialized_data)

@categories.route('/categories/name/<string:name>', methods=['GET'])
def get_category_by_name(name):
    category_data = Category.query.filter_by(name=name).first()
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    category_dict = serialize_category(category_data)

    return jsonify(category_dict), 200

# CREATE a new category, creates a new category with the specified name
@categories.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Missing required field: name'}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    try:
        # Invalidate cache
        redis_cache.redis_client.delete('categories')
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")

    return jsonify({'message': 'Category created successfully'}), 201

# UPDATE an existing category by ID, updates the category with the specified ID
# The new name for the category is specified in the request body
@categories.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Missing required field: name'}), 400

    category_data = Category.query.get(id)
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    category_data.name = name
    db.session.commit()

    try:
        # Invalidate cache
        redis_cache.redis_client.delete(f'category_{id}')
        redis_cache.redis_client.delete('categories')
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")

    return jsonify({'message': 'Category updated successfully'}), 200

# DELETE a category by ID, deletes the category with the specified ID
# If the category does not exist, return a 404 error
@categories.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category_data = Category.query.get(id)
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    db.session.delete(category_data)
    db.session.commit()

    try:
        # Invalidate cache
        redis_cache.redis_client.delete(f'category_{id}')
        redis_cache.redis_client.delete('categories')
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")

    return jsonify({'message': 'Category deleted'}), 200

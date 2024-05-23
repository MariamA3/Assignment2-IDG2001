# Description: This file contains the routes for categories.
# A route is a URL pattern that is associated with a function that is executed when the URL is visited.
# Also called api endpoints.
# This is for the categories table in the database.
# The routes in this file allow users to perform CRUD operations on the categories table.

# Import the Blueprint class from the flask module, which is used to create a Blueprint object
from flask import Blueprint, request, jsonify

# Import the db object from the databaseConnect module
from config.databaseConnect import db

# Import the Category model from the models module
from models.models import Category

# Import RedisCache
from redis_cache import RedisCache

# Create a Blueprint object for categories, which represents the categories routes
categories = Blueprint('categories', __name__)

# GET all categories, returns a list of all categories
@categories.route('/categories', methods=['GET'])
def get_categories():
    # Check if categories are cached
    redis_cache = RedisCache()
    categories_data = redis_cache.get_data('categories')
    if not categories_data:
        categories_data = Category.query.all()
        # Cache categories data for 1 hour (3600 seconds)
        redis_cache.set_data('categories', categories_data, expire=3600)

    categories_list = [
        {
            'category_id': category.category_id,
            'name': category.name
        } for category in categories_data
    ]
    return jsonify(categories_list)

# GET a specific category by ID, returns the category with the specified ID
@categories.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    # Check if category data is cached
    redis_cache = RedisCache()
    category_data = redis_cache.get_data(f'category_{id}')
    if not category_data:
        category_data = Category.query.get(id)

        if not category_data:
            return jsonify({'message': 'Category not found'}), 404
        # Cache category data for 1 hour (3600 seconds)
        redis_cache.set_data(f'category_{id}', category_data, expire=3600)

    category = {
        'category_id': category_data.category_id,
        'name': category_data.name
    }
    return jsonify(category)

@categories.route('/categories/name/<string:name>', methods=['GET'])
def get_category_by_name(name):
    category_data = Category.query.filter_by(name=name).first()
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    category_dict = {
        'category_id': category_data.category_id,
        'name': category_data.name
    }

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

    return jsonify({'message': 'Category deleted'}), 200

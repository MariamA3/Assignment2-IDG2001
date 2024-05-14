from flask import Blueprint, request, jsonify
from config.databaseConnect import db
from models.models import Category

# Create a Blueprint object for categories
categories = Blueprint('categories', __name__)

# GET all categories
@categories.route('/categories', methods=['GET'])
def get_categories():
    categories_data = Category.query.all()
    categories_list = [
        {
            'category_id': category.category_id,
            'name': category.name
        } for category in categories_data
    ]
    return jsonify(categories_list)

# GET a specific category by ID
@categories.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category_data = Category.query.get(id)
    if category_data:
        category = {
            'category_id': category_data.category_id,
            'name': category_data.name
        }
        return jsonify(category)
    return jsonify({'message': 'Category not found'}), 404

# CREATE a new category
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

# UPDATE an existing category by ID
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

# DELETE a category by ID
@categories.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category_data = Category.query.get(id)
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    db.session.delete(category_data)
    db.session.commit()

    return jsonify({'message': 'Category deleted'}), 200

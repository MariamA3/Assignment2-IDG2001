from flask import Blueprint, request, jsonify, current_app

# Create a Blueprint object for categories
categories = Blueprint('categories', __name__)

# Create a function to execute SQL queries
def execute_query(query, params=None, commit=False):
    # Access the database connection from the Flask app context
    db_connection = current_app.config['DB_CONNECTION']

    # Create a cursor object
    cursor = db_connection.cursor()

    # Execute SQL query
    cursor.execute(query, params)

    if commit:
        # Commit changes to the database
        db_connection.commit()
        return

    # Fetch all rows
    data = cursor.fetchall()

    # Close cursor (optional, Flask will handle connection closing)
    cursor.close()

    return data

# GET all categories
@categories.route('/categories', methods=['GET'])
def get_categories():
    categories_data = execute_query("SELECT * FROM categories")
    return jsonify(categories_data)

# GET a specific category by ID
@categories.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category_data = execute_query("SELECT * FROM categories WHERE category_id = %s", (id,))
    if category_data:
        return jsonify(category_data[0])
    return jsonify({'message': 'Category not found'}), 404

# CREATE a new category
@categories.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Missing required field: name'}), 400

    execute_query("INSERT INTO categories (name) VALUES (%s)", (name,))
    
    # Commit the changes to the database
    current_app.config['DB_CONNECTION'].commit()

    return jsonify({'message': 'Category created successfully'}), 201

# UPDATE an existing category by ID
@categories.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Missing required field: name'}), 400

    # Check if the category exists
    category_data = execute_query("SELECT * FROM categories WHERE category_id = %s", (id,))
    if not category_data:
        return jsonify({'message': 'Category not found'}), 404

    # Execute the SQL update query using name variable
    execute_query("UPDATE categories SET name = %s WHERE category_id = %s", (name, id), commit=True)

    return jsonify({'message': 'Category updated successfully'}), 200

# DELETE a category by ID
@categories.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    execute_query("DELETE FROM categories WHERE category_id = %s", (id,), commit=True)
    return jsonify({'message': 'Category deleted'}), 200

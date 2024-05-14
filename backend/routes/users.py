from flask import Blueprint, request, jsonify, current_app

# Create a Blueprint object for users
users = Blueprint('users', __name__)

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

# GET all users
@users.route('/users', methods=['GET'])
def get_users():
    users_data = execute_query("SELECT * FROM users")
    return jsonify(users_data)

# GET a specific user by ID
@users.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user_data = execute_query("SELECT * FROM users WHERE user_id = %s", (id,))
    if user_data:
        return jsonify(user_data[0])
    return jsonify({'message': 'User not found'}), 404

# UPDATE an existing user by ID
@users.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'message': 'Missing required fields: username and email'}), 400

    # Check if the user exists
    user_data = execute_query("SELECT * FROM users WHERE user_id = %s", (id,))
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    # Execute the SQL update query using username and email variables
    execute_query("UPDATE users SET username = %s, email = %s WHERE user_id = %s", (username, email, id), commit=True)

    return jsonify({'message': 'User updated successfully'}), 200

# DELETE a user by ID
## This wont work because the user ID is used as a foreign key in the posts and likes table (referential integrity)
# Might have to look into a fix for this in the future if neccesary
@users.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    execute_query("DELETE FROM users WHERE user_id = %s", (id,), commit=True)
    return jsonify({'message': 'User deleted'}), 200

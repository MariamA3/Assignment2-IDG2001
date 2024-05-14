from flask import Blueprint, request, jsonify, current_app

# Create a Blueprint object for posts
posts = Blueprint('posts', __name__)

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

# GET all posts
@posts.route('/posts', methods=['GET'])
def get_posts():
    posts_data = execute_query("SELECT * FROM posts")
    return jsonify(posts_data)

# GET a specific post by ID
@posts.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post_data = execute_query("SELECT * FROM posts WHERE post_id = %s", (id,))
    if post_data:
        return jsonify(post_data[0])
    return jsonify({'message': 'Post not found'}), 404

# CREATE a new post
@posts.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')
    category_id = data.get('category_id')

    if not title or not content or not user_id or not category_id:
        return jsonify({'message': 'Missing required fields'}), 400

    execute_query("INSERT INTO posts (title, content, user_id, category_id) VALUES (%s, %s, %s, %s)", (title, content, user_id, category_id))
    
    # Commit the changes to the database
    current_app.config['DB_CONNECTION'].commit()

    return jsonify({'message': 'Post created successfully'}), 201

# UPDATE an existing post by ID
@posts.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content are required for updating a post'}), 400

    # Check if the post exists
    post_data = execute_query("SELECT * FROM posts WHERE post_id = %s", (id,))
    if not post_data:
        return jsonify({'message': 'Post not found'}), 404

    # Execute the SQL update query using title and content variables
    execute_query("UPDATE posts SET title = %s, content = %s WHERE post_id = %s", (title, content, id), commit=True)

    return jsonify({'message': 'Post updated successfully'}), 200

# DELETE a post by ID
@posts.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    execute_query("DELETE FROM posts WHERE post_id = %s", (id,), commit=True)
    return jsonify({'message': 'Post deleted'}), 200
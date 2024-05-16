from flask import Blueprint, request, jsonify
from config.databaseConnect import db
from models.models import Post

# Create a Blueprint object for posts
posts = Blueprint('posts', __name__)

# GET all posts
@posts.route('/posts', methods=['GET'])
def get_posts():
    posts_data = Post.query.all()
    posts_list = [
        {
            'post_id': post.post_id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'category_id': post.category_id
        } for post in posts_data
    ]
    return jsonify(posts_list)

# GET a specific post by ID
@posts.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post_data = Post.query.get(id)
    if post_data:
        post = {
            'post_id': post_data.post_id,
            'title': post_data.title,
            'content': post_data.content,
            'user_id': post_data.user_id,
            'category_id': post_data.category_id
        }
        return jsonify(post)
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

    new_post = Post(title=title, content=content, user_id=user_id, category_id=category_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

# UPDATE an existing post by ID
@posts.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content are required for updating a post'}), 400

    post_data = Post.query.get(id)
    if not post_data:
        return jsonify({'message': 'Post not found'}), 404

    post_data.title = title
    post_data.content = content
    db.session.commit()

    return jsonify({'message': 'Post updated successfully'}), 200

# DELETE a post by ID
@posts.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_data = Post.query.get(id)
    if not post_data:
        return jsonify({'message': 'Post not found'}), 404

    db.session.delete(post_data)
    db.session.commit()

    return jsonify({'message': 'Post deleted'}), 200

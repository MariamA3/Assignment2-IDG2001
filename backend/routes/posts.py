from flask import Blueprint, request, jsonify
from datetime import datetime
from config.databaseConnect import db
from models.models import Post
import redis
import json
import logging

# Create a Redis client instance
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_client.ping()  # Test the connection
except redis.exceptions.ConnectionError as e:
    logging.error(f"Redis connection error: {e}")
    redis_client = None

# Create a Blueprint object for posts
posts = Blueprint('posts', __name__)

# Helper function to check Redis connection
def is_redis_connected():
    try:
        if redis_client:
            redis_client.ping()
            return True
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
    return False

# GET all posts
@posts.route('/posts', methods=['GET'])
def get_posts():
    if is_redis_connected():
        try:
            posts_data = redis_client.get('posts')
            if posts_data:
                return jsonify(json.loads(posts_data))

            posts_data = Post.query.all()
            posts_list = [
                {
                    'post_id': post.post_id,
                    'title': post.title,
                    'content': post.content,
                    'user_id': post.user_id,
                    'category_id': post.category_id,
                    'created_at': post.created_at.isoformat() if post.created_at else None
                } for post in posts_data
            ]

            redis_client.set('posts', json.dumps(posts_list), ex=900)  # Cache for 15 min
            return jsonify(posts_list)
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")

    # Fallback to database query if Redis is not available
    posts_data = Post.query.all()
    posts_list = [
        {
            'post_id': post.post_id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'category_id': post.category_id,
            'created_at': post.created_at.isoformat() if post.created_at else None
        } for post in posts_data
    ]
    return jsonify(posts_list)

# GET a specific post by ID
@posts.route('/posts/id/<int:id>', methods=['GET'])
def get_post(id):
    if is_redis_connected():
        try:
            post_data = redis_client.get(f'post_{id}')
            if post_data:
                return jsonify(json.loads(post_data))

            post_data = Post.query.get(id)
            if post_data:
                post = {
                    'post_id': post_data.post_id,
                    'title': post_data.title,
                    'content': post_data.content,
                    'user_id': post_data.user_id,
                    'category_id': post_data.category_id,
                    'created_at': post_data.created_at.isoformat() if post_data.created_at else None
                }
                redis_client.set(f'post_{id}', json.dumps(post), ex=900)  # Cache for 15 min
                return jsonify(post)
            return jsonify({'message': 'Post not found'}), 404
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")

    # Fallback to database query if Redis is not available
    post_data = Post.query.get(id)
    if post_data:
        post = {
            'post_id': post_data.post_id,
            'title': post_data.title,
            'content': post_data.content,
            'user_id': post_data.user_id,
            'category_id': post_data.category_id,
            'created_at': post_data.created_at.isoformat() if post_data.created_at else None
        }
        return jsonify(post)
    return jsonify({'message': 'Post not found'}), 404

# GET all posts for a specific category
@posts.route('/posts/category/<int:category_id>', methods=['GET'])
def get_posts_by_category(category_id):
    post_data = Post.query.filter_by(category_id=category_id).all()
    if post_data:
        posts = [{
            'post_id': post.post_id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'category_id': post.category_id,
            'created_at': post.created_at.isoformat() if post.created_at else None
        } for post in post_data]
        return jsonify(posts)
    return jsonify({'message': 'No posts found for this category'}), 404

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

    new_post = Post(
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
        created_at=datetime.utcnow()  # Manually set the creation time to UTC now
    )
    db.session.add(new_post)
    db.session.commit()

    if is_redis_connected():
        try:
            redis_client.delete('posts')
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")

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

    if is_redis_connected():
        try:
            redis_client.delete(f'post_{id}')
            redis_client.delete('posts')
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")

    return jsonify({'message': 'Post updated successfully'}), 200

# DELETE a post by ID
@posts.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_data = Post.query.get(id)
    if not post_data:
        return jsonify({'message': 'Post not found'}), 404

    db.session.delete(post_data)
    db.session.commit()

    if is_redis_connected():
        try:
            redis_client.delete(f'post_{id}')
            redis_client.delete('posts')
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")

    return jsonify({'message': 'Post deleted'}), 200

# LIKE a post
@posts.route('/posts/like/<int:id>', methods=['POST'])
def like_post(id):
    user_id = request.json.get('user_id')
    if user_id:
        if is_redis_connected():
            try:
                like_data = {'user_id': user_id, 'post_id': id}
                redis_client.rpush('pending_likes', json.dumps(like_data))
                return jsonify({'message': 'Like queued successfully'}), 200
            except redis.exceptions.ConnectionError as e:
                logging.error(f"Redis connection error: {e}")
                return jsonify({'message': 'Like could not be queued'}), 500
        else:
            return jsonify({'message': 'Redis not connected'}), 500
    return jsonify({'message': 'User ID is required'}), 400

# UNLIKE a post
@posts.route('/posts/unlike/<int:id>', methods=['POST'])
def unlike_post(id):
    user_id = request.json.get('user_id')
    if user_id:
        if is_redis_connected():
            try:
                like_data = {'user_id': user_id, 'post_id': id}
                redis_client.lrem('pending_likes', 0, json.dumps(like_data))
                return jsonify({'message': 'Unlike queued successfully'}), 200
            except redis.exceptions.ConnectionError as e:
                logging.error(f"Redis connection error: {e}")
                return jsonify({'message': 'Unlike could not be queued'}), 500
        else:
            return jsonify({'message': 'Redis not connected'}), 500
    return jsonify({'message': 'User ID is required'}), 400

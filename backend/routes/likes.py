from flask import Blueprint, request, jsonify
import redis
import json
import os
import logging

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

# Create a Blueprint object for likes, with the /api prefix
likes = Blueprint('likes', __name__, url_prefix='/api')

@likes.route('/like', methods=['POST'])
def like_post():
    data = request.json
    if 'user_id' not in data or 'post_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        # Enqueue the like in Redis
        redis_client.rpush('pending_likes', json.dumps(data))
        return jsonify({'status': 'Like enqueued'}), 200
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
        return jsonify({'error': 'Could not enqueue like'}), 500

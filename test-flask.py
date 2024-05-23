from flask import Flask, jsonify
from redis_cache import RedisCache

app = Flask(__name__)
redis_cache = RedisCache()

@app.route('/test-redis')
def test_redis():
    # Set a test key-value pair in Redis
    redis_cache.set_data('test_key', 'test_value')
    
    # Retrieve the value from Redis
    value = redis_cache.get_data('test_key')

    # Return the retrieved value as a JSON response
    return jsonify({'value': value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

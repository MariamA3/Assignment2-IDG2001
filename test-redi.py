import redis

# Redis connection
redis_host = 'redis'
redis_port = 6379

# Attempt to connect to Redis
try:
    redis_client = redis.Redis(host=redis_host, port=redis_port)
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Error connecting to Redis: {e}")

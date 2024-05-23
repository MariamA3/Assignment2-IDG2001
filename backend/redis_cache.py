# redis connection module 
#to connect redis to python 
# redis_cache.py
import redis
import json
import os

class RedisCache:
    def __init__(self, host=None, port=None, db=0):
        self.redis_host = host or os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = port or int(os.getenv('REDIS_PORT', 6379))
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=db)
        print(f"Connecting to Redis at {self.redis_host}:{self.redis_port}")
        try:
            self.redis_client.ping()
            print("Successfully connected to Redis!")
        except redis.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")

    def set_data(self, key, value, expire=3600):
        value_json = json.dumps(value)
        self.redis_client.setex(key, expire, value_json)

    def get_data(self, key):
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

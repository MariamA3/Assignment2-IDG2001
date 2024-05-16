# redis connection module 
#to connect redis to python 

import redis

class RedisCache:
    def __init__(self, host='redis', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def set_data(self, key, value):
        self.redis_client.set(key, value)

    def get_data(self, key):
        return self.redis_client.get(key)

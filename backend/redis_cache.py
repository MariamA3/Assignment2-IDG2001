# redis connection module 
#to connect redis to python 

#DENNE ER NY 
import redis
import json

class RedisCache:
    def __init__(self, host='redis', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def set_data(self, key, value, expire=3600):
        value_json = json.dumps(value)
        self.redis_client.setex(key, expire, value_json)

    def get_data(self, key):
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

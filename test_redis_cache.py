import pytest
import redis
from backend.redis_cache import RedisCache
from unittest.mock import patch
import json

@pytest.fixture
def redis_cache():
    with patch.object(RedisCache, '__init__', lambda x: None):
        redis_cache_instance = RedisCache()
        redis_cache_instance.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        yield redis_cache_instance

def test_set_data(redis_cache):
    key = 'test_key'
    value = {'name': 'Test'}
    expire = 3600

    redis_cache.set_data(key, value, expire)
    stored_value = redis_cache.redis_client.get(key)

    assert stored_value is not None
    assert json.loads(stored_value) == value

def test_get_data(redis_cache):
    key = 'test_key'
    value = {'name': 'Test'}
    redis_cache.redis_client.set(key, '{"name":"Test"}')
    
    retrieved_value = redis_cache.get_data(key)
    
    assert retrieved_value == value

def test_get_data_not_exists(redis_cache):
    key = 'nonexistent_key'
    
    retrieved_value = redis_cache.get_data(key)
    
    assert retrieved_value is None

def test_set_data_with_expiry(redis_cache):
    key = 'test_expiry_key'
    value = {'expiry': 'Test'}
    expire = 1  # 1 second for test

    redis_cache.set_data(key, value, expire)
    stored_value = redis_cache.redis_client.get(key)

    assert stored_value is not None
    assert json.loads(stored_value) == value

# Mock Redis connection errors
def test_set_data_redis_connection_error(redis_cache):
    with patch.object(redis_cache.redis_client, 'setex', side_effect=redis.ConnectionError("Redis connection error")):
        try:
            redis_cache.set_data('key', 'value', 3600)
        except redis.ConnectionError as e:
            assert str(e) == 'Redis connection error'

def test_get_data_redis_connection_error(redis_cache):
    with patch.object(redis_cache.redis_client, 'get', side_effect=redis.ConnectionError("Redis connection error")):
        try:
            redis_cache.get_data('key')
        except redis.ConnectionError as e:
            assert str(e) == 'Redis connection error'

if __name__ == "__main__":
    pytest.main()

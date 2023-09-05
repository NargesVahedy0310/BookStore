import redis
import time
class RedisClient:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def update_cache(self, key, new_value):
        self.client.set(key,new_value, 30, time.time())

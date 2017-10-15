__author__ = 'tintin'

import redis

class RedisService():
    def __init__(self):
        self.redisConnection = redis.Redis("localhost")

    def getConnection(self):
        return self.redisConnection
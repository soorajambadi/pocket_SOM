from tmodels.SOMNode import SOMNode
from transformers.RedisPy import convertToString
from transformers.RedisSaver import saveToRedis

__author__ = 'tintin'

# Initialize SOM Network in Redis
def createSOM(m, n):
    for i in xrange(m):
        for j in xrange(n):
            saveToRedis.delay(str(i*m+n), convertToString(SOMNode(i, j)))
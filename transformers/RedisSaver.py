__author__ = 'tintin'

from manager.celery import app, getworkerManager

@app.task
def saveToRedis(key, value):
    getworkerManager().getRedisInstance().getConnection().set(key, value)
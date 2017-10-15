from manager.RedisService import RedisService

__author__ = 'tintin'

from bottle import run, Bottle, redirect
from storedb.database import Database
from crawler.scrap import Crawler

''' We design it such that ask for an instance, we return the celery instance. So we can run tasks on celery instance
just like a database or crawler instance. '''


class Manager():
    # global databaseService
    # global crawlerService

    def __init__(self):
        # Services or Connections for database and crawler
        self.databaseService = Database("http://localhost:7474/db/data/", "neo4j", "jvc")
        self.crawlerService = Crawler()
        self.redisService = RedisService()

    def getDatabaseInstance(self):
        return self.databaseService

    def getCrawlerInstance(self):
        return self.crawlerService

    def getRedisInstance(self):
        return self.redisService
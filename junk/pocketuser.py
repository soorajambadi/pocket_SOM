# -*- coding: utf-8 -*-
from storedb.database import NodeCreateException

class PocketUser:

    def __init__(self, username, engine):
        self.username = username
        self.engine = engine
        # You need to make sure you have a connection to database
        # Make a node for this user if not in the database
        try:
            self.userid = engine.database.getElseMakeUser(username)
        except NodeCreateException, ex:
            print ((ex.msg))
            # Exception when unable to create user

    def setEngine(self, engine):
        self.engine = engine

    def getRecommendations(self, engine=None):
        # This is for supporting multiples engines for the same user
        try:
            if engine is not None:
                self.results = engine.getRecommendations(self)
                #need to test if this is correct
                return self.results
            else:
                self.results = self.engine.getRecommendations(self)
        except:
            pass
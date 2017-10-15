# -*- coding: utf-8 -*-
from storedb.database import TagException

class Engine():

    def __init__(self, database, algorithm):
        self.database = database
        self.algorithm = algorithm

    def GetRecommendations(self, pocketuser):
        # pocketuser is of type PocketUser
        pass
        # Insert Engine specific code Here

    def GetUserTags(self, userid):
        # It is passed the userid of the user in the database
        try:
            tags = self.database.GetUserTags(userid)
            return tags
        except TagException, ex:
            print ((ex.msg))

    def GetUserLinksFromTag(self, userid, tag):
        # It is passed the userid of the user in the database
        try:
            links = self.database.GetUserLinksFromTag(userid, tag)
            return links
        except TagException, ex:
            print ((ex.msg))

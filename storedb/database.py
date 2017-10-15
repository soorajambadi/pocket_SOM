# -*- coding: utf-8 -*-
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

##########Exception Handlers############


class DatabaseException(Exception):
    pass
    # Base class Exception for all Database related errors


class TagException(DatabaseException):

    def __init__(self, msg):
        self.msg = msg
    # All Tag related Exceptions


class UserException(DatabaseException):

    def __init__(self, msg):
        self.msg = msg
    # All User related Exceptions


class LinkException(DatabaseException):

    def __init__(self, msg):
        self.msg = msg
    #All Links related Exceptions


class NodeCreateException(DatabaseException):

    def __init__(self, msg):
        self.msg = msg
    # Exceptions related to Node creation failures in database
#########End of Exceptions ##########


class Database():

    def __init__(self, serverUrl, serverUserName=None, serverPassword=None):
        # If possible employ a connection failure handler
        self.gdb = GraphDatabase(serverUrl, username=serverUserName, password=serverPassword)
        #self.gdb = GraphDatabase(serverUrl)
        # Below we don't take care of index creation and access exceptions
        try:
            self.userindex = self.gdb.nodes.indexes.get("UserIndex")
        except:
            self.userindex = self.gdb.nodes.indexes.create("UserIndex")
        try:
            self.globtags = self.gdb.nodes.indexes.get("GlobalTags")
        except:
            self.globtags = self.gdb.nodes.indexes.create("GlobalTags")
        # globtags represents global Tags
        try:
            self.webindex = self.gdb.nodes.indexes.get("WebPageIndex")
        except:
            self.webindex = self.gdb.nodes.indexes.create("WebPageIndex")
        # webpages represents Global WebPageIndex

    def GetallLinks(self):
        return self.gdb.nodes.indexes.get("WebPageIndex")

    def GetUserTags(self, userid):
        try:
            inter = userid
            # This is to specify that inter represents intermediate
            result = inter.traverse(types=client.Outgoing.Tags)
            return result
        except:
            raise DatabaseException("Exception in GetUserTags")
            # Change later

    def GetUserLinksFromTag(self, userid, tagname):
        #why we use create here ?
        # I'm changing create to get
        inter = self.gdb.nodes.get(username=userid)
        inter2 = inter.traverse(types=client.Outgoing.Tags)
        # inter2 represents it is intermediate output 2
        for link in inter2:
            if tagname == link.properties['Tag']:
                result = link.traverse(types=client.Outgoing.ParentOf)
                if result:
                    return result
                else:
                    raise LinkException("No links associated with the tag")
                    # Exception represents no links with those tags
        raise TagException("No such tag associated with the user")
        # Exception represents no such tag associated with the user

    def getElseMakeUser(self, username):
        try:
            if self.userindex["username"][username][0]:
                return self.userindex["username"][username][0]
        except:
            try:
                result = self.gdb.nodes.create(username=username)
                # We store users in nodes with attribute username
                self.userindex["username"][username] = result
                return result
            except:
                raise NodeCreateException("Unable to create User Node ")
                # Raise exception when unable to create usernode

    def MakeUserTagNode(self, userid, tagname):
        inter = userid
        inter2 = inter.traverse(types=client.Outgoing.Tags)
        # inter2 represents it is intermediate output 2
        tagfound = False
        #initialize ftagnode to null
        ftagnode = None
        #Used to represent if the tag node already exists
        for tagnode in inter2:
            if tagname == tagnode.properties['Tag']:
                tagfound = True
                ftagnode = tagnode
                break
        if not tagfound:
            try:
                tagnode = self.gdb.nodes.create(Tag=tagname)
                # tagnode represents the new tagnode made
                self.globtags["tagname"][tagname] = tagnode
                # Don't know whether it works, anyway we visualize global tag
                # Handle index here
                inter.relationships.create("Tags", tagnode)
                return tagnode
            except:
                raise NodeCreateException("Unable to create Tag Node ")
        return ftagnode

        # We are returning tagnode as we plan to make a global tag node connecting
        # all local tag nodes

    def MakeFriendRelationship(self, nodeid1, nodeid2):
        node1 = self.gdb.nodes.get(nodeid1)
        node2 = self.gdb.nodes.get(nodeid2)
        node1.relationships.create(node2, "FriendOf")
        # need to check if it is efficient
        # also need to make sure if something is needed to be added

    def MakeWebPageNode(self, username, url, title, content, tags):
        # The passed are the url, title and content of a webpage
        if self.webindex["page"][url]:
            result = self.webindex["page"][url][0]
        else:
            try:
                result = self.gdb.nodes.create(weburl=url, title=title, content=content)
                # We store users in nodes with attribute username
                self.webindex["page"][url] = result
                return result
            except:
                raise NodeCreateException("Unable to create WebPage Node ")
                # Raise exception when unable to create webpage node
        node1 = self.getElseMakeUser(username)
        for tag in tags:
            try:
                tagnode = self.MakeUserTagNode(node1, tag)
                tagnode.relationships.create("ParentOf", result)
            except NodeCreateException as ex:
                print (ex.msg)
                raise NodeCreateException(ex.msg)
        print("Data Entered to Database")
        return result

# Need to make provision for deletion of tags
# Make Tag Index for each user
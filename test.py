# -*- coding: utf-8 -*-
from storedb.database import Database
from engine.engine import Engine
from junk.pocketuser import PocketUser
from crawler.scrap import Crawler, WebPage


db = Database("http://localhost:7474/db/data/", serverUserName="neo4j", serverPassword="jvc")
en = Engine(db, 0)
pu = PocketUser("Hia", en)
print pu
pu2 = PocketUser("Hia2", en)
print pu2
print pu.userid
print pu2.userid
print pu.engine.database.MakeUserTagNode(pu.userid, "India2")
print pu2.engine.database.MakeUserTagNode(pu2.userid, "India2")
crawler = Crawler()
#webpage = WebPage("https://en.wikipedia.org/wiki/Linux", crawler)
#webpage.get_page_contents()
#print webpage.content
#print webpage.title
webpage = WebPage("http://reviewglitz.com/", crawler)
webpage.get_page_contents()
print webpage.content
print webpage.title
db.MakeWebPageNode(pu.username, webpage.url, webpage.title, webpage.content,
list(("linux", "love")))
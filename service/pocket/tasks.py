__author__ = 'tintin'

from manager.celery import app
# import the Celery log getter
from celery.utils.log import get_task_logger
from manager.Manager import Manager
# grab the logger for the Celery app
logger = get_task_logger(__name__)
import json
from celery.contrib import rdb

@app.task
def fetchandsavepage(links, username):
    database = Manager.getDatabaseInstance()
    crawler = Manager.getCrawlerInstance()
    database.getElseMakeUser(username)
    print ("Database Made")
    #rdb.set_trace()
    links = json.loads(links)
    links = links['list'].values()
    for link in links:
        try:
            if not crawler:
                crawler = Manager.getCrawlerInstance()
            else:
                page = crawler.make_a_page(link['resolved_url'])
                page.get_page_contents()
                # need a method to generate tags
                tags = ["jvc", "pocket"]
                database.MakeWebPageNode(username, link['resolved_url'],
                page.title, page.content, tags)
                print ("Hardware Done")
                print (page.url)
                #print self.page.content
                print (page.title)
        except:
            print("Exception occured")
            continue
    print("Fetching Articles code here")
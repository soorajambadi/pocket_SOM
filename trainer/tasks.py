__author__ = 'tintin'

from manager.celery import app
# import the Celery log getter
from celery.utils.log import get_task_logger
from manager.Manager import Manager
# grab the logger for the Celery app
logger = get_task_logger(__name__)

# we pass in a list here
@app.task
def trainSOM(contentlist):
    # train your som in celery here
    print "In task"

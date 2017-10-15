from __future__ import absolute_import
from celery import Celery

# instantiate Celery object
# add more celery tasks
from celery.signals import worker_process_init
from manager.Manager import Manager

app = Celery(include=[
    'messaging.tasks',
    'service.pocket.tasks',
    'transformers.RedisSaver'
])

# import celery config file
app.config_from_object('celeryconfig')

# global Manager for celery worker
workerManager = None

# Executes when a worker is initialized
@worker_process_init.connect
def init_worker(**kwargs):
    # To access global Manager
    global workerManager
    workerManager = Manager()
    print " In worker " + str(workerManager)


def getworkerManager():
    global workerManager
    print "In getWorkerManager " + str(workerManager)
    if workerManager:
        return workerManager
    else:
        print "Why is it null ?"
        return None


if __name__ == '__main__':
    app.start()
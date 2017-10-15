__author__ = 'tintin'

from manager.celery import app
# import the Celery log getter
from celery.utils.log import get_task_logger

# grab the logger for the Celery app
logger = get_task_logger(__name__)

@app.task
def fetchListFromPocket(url):
    print(url)
    print("Fetching Articles code here")

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
    logger.info("result of x is " + results.__str__())
    print(results.__str__())
    return results
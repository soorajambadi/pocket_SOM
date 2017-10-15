__author__ = 'tintin'

import cPickle

# Convert Python object to String using Json
def convertToString(obj):
    return cPickle.dumps(obj)

# Convert json to python object
def convertToObject(string):
    return cPickle.loads(string)
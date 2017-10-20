import sys
import config
from tornado.gen import coroutine

class InsertObject(object):

    def __init__(self, con):
        try:
            self._db = con[config.db_name]
            self._collection = self._db[config.collection_name]
        except:
            print("error::__init>>", sys.exc_info()[1])

    @coroutine
    def InsertOne(self, data):
        try:
            self._collection.insert_one(data)
        except:
            print("error::InsertOne>>", sys.exc_info()[1])


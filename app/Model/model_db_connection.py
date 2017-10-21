import sys
import config as config
import pymongo

# con = pymongo.MongoClient(host=config.host, port=config.port)
class InsertObject(object):

    def __init__(self, con):
        try:
            self._db = con[config.db_name]
            self._collection = self._db[config.collection_name]
        except:
            print("error::__init>>", sys.exc_info()[1])

    def InsertOne(self, data):
        try:
            self._collection.insert(data)
        except:
            print("error::InsertOne>>", sys.exc_info()[1])


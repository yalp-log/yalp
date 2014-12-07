# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.mongo
==================
'''
import pymongo
from . import BaseOutputer


class MongoOutputer(BaseOutputer):
    '''
    Send output to mongo.
    '''
    def __init__(self,
                 uri,
                 database,
                 collection,
                 *args,
                 **kwargs):
        super(MongoOutputer, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def output(self, event):
        self.collection.insert(event)

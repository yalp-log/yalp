# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.mongo
==================

The mongo outputer sends events to a mongo collection. Each event
is recorded as a new document in the collection.

This outputer supports the following configuration items:

**uri**
    The mongodb connection uri. Formatted as
    ``mongodb://[user:password@]<host>[:port]/[auth_database]``

**database**
    The database name to store the documents.

**collection**
    The collection name.

*type*
    A type filter. Only output events of this type.

Example configuration.

.. code-block:: yaml

    outputs:
      - mongo:
          uri: 'mongodb://localhost:27017/yalp'
          database: yalp
          collection: logs

'''
import pymongo
from . import BaseOutputer


class Outputer(BaseOutputer):
    '''
    Send output to mongo.
    '''
    def __init__(self,
                 uri,
                 database,
                 collection,
                 *args,
                 **kwargs):
        super(Outputer, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def output(self, event):
        self.collection.insert(event)

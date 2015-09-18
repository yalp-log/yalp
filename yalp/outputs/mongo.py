# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.mongo
==================

The mongo outputer sends events to a mongo collection. Each event
is recorded as a new document in the collection.

.. warning:: This requires the pymongo_ pacakge to be installed.

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

.. _pymongo: https://pypi.python.org/pypi/pymongo/
'''
try:
    import pymongo
except ImportError:  # pragma: no cover
    pass
from . import BaseOutputer


class MongoDBOutputer(BaseOutputer):
    '''
    Send output to mongo.
    '''
    def __init__(self,
                 uri,
                 database,
                 collection,
                 *args,
                 **kwargs):
        super(MongoDBOutputer, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def output(self, event):
        self.collection.insert(event)

    def shutdown(self):
        self.client.fsync()
        self.client.close()


Outputer = MongoDBOutputer

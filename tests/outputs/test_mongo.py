# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.outputs.test_mongo
========================
'''
import unittest
from yalp.outputs import mongo


class TestMongoOutput(unittest.TestCase):
    '''
    Test the mongo.Outputer
    '''
    def setUp(self):
        self.config = {
            'uri': 'mongodb://localhost/',
            'database': 'yalp_test',
            'collection': 'test_collection'
        }
        try:
            import pymongo
            self.client = pymongo.MongoClient(self.config['uri'])
            self.database = self.client[self.config['database']]
            self.database.drop_collection(self.config['collection'])
        except (ImportError, pymongo.errors.ConnectionFailure):
            from nose.plugins.skip import SkipTest
            raise SkipTest('pymongo not installed')

    def tearDown(self):
        self.database.drop_collection(self.config['collection'])
        self.client.close()

    def test_output_event(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
        }
        outputer = mongo.Outputer(
            uri=self.config['uri'],
            database=self.config['database'],
            collection=self.config['collection']
        )
        outputer.run(event)
        collection = self.database[self.config['collection']]
        outputs = collection.find()
        self.assertEqual(outputs.count(), 1)
        self.assertEqual(outputs[0], event)

    def test_output_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no mongo',
        }
        outputer = mongo.Outputer(
            uri=self.config['uri'],
            database=self.config['database'],
            collection=self.config['collection']
        )
        outputer.run(event)
        collection = self.database[self.config['collection']]
        outputs = collection.find()
        self.assertEqual(outputs.count(), 0)

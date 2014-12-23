# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.outputs.test_elasticsearch
========================
'''
import unittest
from yalp.outputs import elasticsearch


class TestElasticsearchOutput(unittest.TestCase):
    '''
    Test the elasticsearch.Outputer
    '''
    def setUp(self):
        self.config = {
            'uri': 'http://localhost:9200/',
            'index': 'yalp_test',
            'doc_type': 'test_doc'
        }
        try:
            import elasticsearch as es_dep
            self.es = es_dep.Elasticsearch(self.config['uri'])
            self.index = self.config['index']
            self.doc_type = self.config['doc_type']
            self.es.indices.delete('*')
            self.es.indices.create(index=self.index, ignore=400)
        except (ImportError, es_dep.ConnectionError):
            from nose.plugins.skip import SkipTest
            raise SkipTest('Unable to connect to Elasticsearch')

    def tearDown(self):
        self.es.indices.delete('*')

    def test_output_event(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
        }
        outputer = elasticsearch.Outputer(
            uri=self.config['uri'],
            index=self.config['index'],
            doc_type=self.config['doc_type']
        )
        outputer.run(event)
        outputer.shutdown()
        count = self.es.count(self.index, self.doc_type).get('count')
        self.assertEqual(count, 1)

    def test_output_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no elasticsearch',
        }
        outputer = elasticsearch.Outputer(
            uri=self.config['uri'],
            index=self.config['index'],
            doc_type=self.config['doc_type']
        )
        outputer.run(event)
        outputer.shutdown()
        count = self.es.count(self.index, self.doc_type).get('count')
        self.assertEqual(count, 0)

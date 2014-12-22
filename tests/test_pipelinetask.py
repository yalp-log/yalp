# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_pipelinetask
=======================
'''
import unittest
from yalp.pipeline.tasks import PipelineTask
from yalp.config import settings


class TestPipelineTaskProperties(unittest.TestCase):
    '''
    Test properties on PipelineTask
    '''
    def setUp(self):
        settings.parsers = []
        settings.outputs = []

    def tearDown(self):
        settings.parsers = []
        settings.outputs = []

    def test_parsers_property(self):
        ''' test getting parsers via property '''
        settings.parsers = [{
            'passthrough': {}
        }]
        task = PipelineTask()
        parsers = task.parsers
        from yalp.parsers.passthrough import Parser
        self.assertEqual(len(parsers), 1)
        for parser in parsers:
            self.assertIsInstance(parser, Parser)

    def test_multi_parsers(self):
        ''' test getting multiple parsers via property '''
        settings.parsers = [
            {
                'passthrough': {}
            },
            {
                'regex': {
                    'regex': 'blah',
                }
            },
        ]
        task = PipelineTask()
        parsers = task.parsers
        self.assertEqual(len(parsers), 2)
        from yalp.parsers.passthrough import Parser as PassthroughParser
        from yalp.parsers.regex import Parser as RegexParser
        self.assertIsInstance(parsers[0], PassthroughParser)
        self.assertIsInstance(parsers[1], RegexParser)

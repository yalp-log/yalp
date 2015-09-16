# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_chained
==========================
'''
import unittest
from yalp.config import settings
from yalp.pipeline.tasks import process_message


class TestChainedParsers(unittest.TestCase):
    '''
    Test that the parser task correctly applies a chain of parsers.
    '''
    def setUp(self):
        parser_config = {
            'parsers': [
                {
                    'grok': {
                        'pattern': '%{COMBINEDAPACHELOG}',
                    }
                },
                {
                    'timestamp': {
                        'field': 'timestamp',
                    }
                }
            ]
        }
        settings.update(parser_config)
        process_message.reload_config()

    def test_chain(self):
        event = {
            'message': '127.0.0.1 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-01-01T01:00:00',
            'hostname': 'server_hostname',
        }
        expected = {
            'message': '127.0.0.1 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-09-15T13:41:35',
            'hostname': 'server_hostname',
            'clientip': '127.0.0.1',
            'ident': '-',
            'auth': '-',
            'timestamp': '15/Sep/2015:13:41:35 -0400',
            'verb': 'GET',
            'request': '/index.html',
            'rawrequest': None,
            'httpversion': '1.1',
            'response': '200',
            'bytes': '352',
            'referrer': '"-"',
            'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        }
        processed_event = process_message(event)
        self.assertDictEqual(expected, processed_event)

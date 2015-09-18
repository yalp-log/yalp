# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_url
======================
'''
import unittest
from yalp.parsers import url


class TestUrlParser(unittest.TestCase):
    '''
    Test the url.Parser
    '''
    def test_parse_event(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'request': '/index.html?param1=val1&param2=val2',
        }
        parser = url.Parser()
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'request': '/index.html?param1=val1&param2=val2',
            'url': {
                'fragment': '',
                'hostname': None,
                'netloc': '',
                'params': '',
                'password': None,
                'path': '/index.html',
                'port': None,
                'query': {
                    'param1': ['val1'],
                    'param2': ['val2'],
                },
                'scheme': '',
                'username': None
            },
        }
        self.assertDictEqual(expected, parsed_event)

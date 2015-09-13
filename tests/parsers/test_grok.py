# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_grok
=======================
'''
import unittest
from yalp.parsers import grok


class TestGrokParser(unittest.TestCase):
    '''
    Test the grok.Parser
    '''

    def test_parse_event(self):
        event = {
            'message': '192.168.0.1 GET /index.html',
            'time_stamp': '2015-01-01T01:00:00',
            'hostname': 'server_hostname',
        }
        parser = grok.Parser(
            pattern='%{IP:ip_addr} %{WORD:request_type} %{URIPATHPARAM:path}'
        )
        parsed_event = parser.run(event)
        expected = {
            'message': '192.168.0.1 GET /index.html',
            'time_stamp': '2015-01-01T01:00:00',
            'hostname': 'server_hostname',
            'ip_addr': '192.168.0.1',
            'request_type': 'GET',
            'path': '/index.html',
        }
        self.assertDictEqual(expected, parsed_event)

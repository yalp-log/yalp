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

    def test_nginx_event(self):
        event = {
            'message': '127.0.0.1 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-01-01T01:00:00',
            'hostname': 'server_hostname',
        }
        parser = grok.Parser(
            pattern='%{COMBINEDAPACHELOG}'
        )
        parsed_event = parser.run(event)
        expected = {
            'message': '127.0.0.1 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-01-01T01:00:00',
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
        self.assertDictEqual(expected, parsed_event)

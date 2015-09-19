# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_chained
==========================
'''
import os
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


class TestLongChain(unittest.TestCase):
    '''
    Test that the parser task chains completely.
    '''
    def setUp(self):
        self.maxDiff = None
        self.test_dat_file = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'GeoLiteCity.dat',
        ))
        if not os.path.isfile(self.test_dat_file):
            from nose.plugins.skip import SkipTest
            raise SkipTest('No GeoLiteCity dat file')
        parser_config = {
            'parsers': [
                {'grok': {'pattern': '%{COMBINEDAPACHELOG}'}},
                {'timestamp': {'field': 'timestamp'}},
                {'geoip': {
                    'field': 'clientip',
                    'geoip_dat': self.test_dat_file
                }},
                {'user_agent': {'field': 'agent'}},
                {'url': {'field': 'request'}},
            ]
        }
        settings.update(parser_config)
        process_message.reload_config()

    def test_long_chain(self):
        event = {
            'message': '8.8.4.4 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html?param=val HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-01-01T01:00:00',
            'hostname': 'server_hostname',
        }
        expected = {
            'message': '8.8.4.4 - - [15/Sep/2015:13:41:35 -0400] "GET /index.html?param=val HTTP/1.1" 200 352 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'time_stamp': '2015-09-15T13:41:35',
            'hostname': 'server_hostname',
            'clientip': '8.8.4.4',
            'ident': '-',
            'auth': '-',
            'timestamp': '15/Sep/2015:13:41:35 -0400',
            'verb': 'GET',
            'request': '/index.html?param=val',
            'rawrequest': None,
            'httpversion': '1.1',
            'response': '200',
            'bytes': '352',
            'referrer': '"-"',
            'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'browser': {'family': 'Firefox', 'version': '38'},
            'device': {'brand': None, 'family': 'Other', 'model': None},
            'os': {'family': 'Linux', 'version': ''},
            'is_bot': False,
            'is_mobile': False,
            'is_pc': True,
            'is_tablet': False,
            'is_touch_capable': False,
            'geoip': {'area_code': 0,
                      'city': None,
                      'continent': 'NA',
                      'country_code': 'US',
                      'country_code3': 'USA',
                      'country_name': 'United States',
                      'dma_code': 0,
                      'location': '9yg00twy01mt',
                      'metro_code': None,
                      'postal_code': None,
                      'region_code': None,
                      'time_zone': None},
            'url': {'fragment': '',
                    'hostname': None,
                    'netloc': '',
                    'params': '',
                    'password': None,
                    'path': '/index.html',
                    'port': None,
                    'query': {'param': ['val']},
                    'scheme': '',
                    'username': None},
        }
        processed_event = process_message(event)
        self.assertDictEqual(expected, processed_event)

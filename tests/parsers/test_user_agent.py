# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_user_agent
=============================
'''
import unittest
from yalp.parsers import user_agent


class TestUserAgentParser(unittest.TestCase):
    '''
    Test the user_agent.Parser
    '''

    def test_parse_event(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        }
        parser = user_agent.Parser()
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'os': {'family': 'Linux', 'version': ''},
            'browser': {'family': 'Firefox', 'version': '38'},
            'device': {'brand': None, 'family': 'Other', 'model': None},
            'is_bot': False,
            'is_mobile': False,
            'is_pc': True,
            'is_tablet': False,
            'is_touch_capable': False,
        }
        self.assertDictEqual(expected, parsed_event)

    def test_missing_field(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        }
        parser = user_agent.Parser()
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        }
        self.assertDictEqual(expected, parsed_event)

    def test_not_agent_str(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': '"not a user agent str"',
        }
        parser = user_agent.Parser()
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': '"not a user agent str"',
            'os': {'family': 'Other', 'version': ''},
            'browser': {'family': 'Other', 'version': ''},
            'device': {'brand': None, 'family': 'Other', 'model': None},
            'is_bot': False,
            'is_mobile': False,
            'is_pc': False,
            'is_tablet': False,
            'is_touch_capable': False,
        }
        self.assertDictEqual(expected, parsed_event)

    def test_out_field(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        }
        parser = user_agent.Parser(out_field='agent')
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
            'agent': {
                'os': {'family': 'Linux', 'version': ''},
                'browser': {'family': 'Firefox', 'version': '38'},
                'device': {'brand': None, 'family': 'Other', 'model': None},
                'is_bot': False,
                'is_mobile': False,
                'is_pc': True,
                'is_tablet': False,
                'is_touch_capable': False,
            },
        }
        self.assertDictEqual(expected, parsed_event)

    def test_nested(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'url': {
                'query': {
                    'ua': ['"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"'],
                }
            }
        }
        parser = user_agent.Parser(field='url:query:ua:0', out_field='agent')
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'url': {
                'query': {
                    'ua': ['"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"'],
                }
            },
            'agent': {
                'os': {'family': 'Linux', 'version': ''},
                'browser': {'family': 'Firefox', 'version': '38'},
                'device': {'brand': None, 'family': 'Other', 'model': None},
                'is_bot': False,
                'is_mobile': False,
                'is_pc': True,
                'is_tablet': False,
                'is_touch_capable': False,
            },
        }
        self.assertDictEqual(expected, parsed_event)

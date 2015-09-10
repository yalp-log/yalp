# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.parsers.test_passthrough
=============================
'''
import unittest
from yalp.parsers import passthrough


class TestPassthroughParser(unittest.TestCase):
    '''
    Test the passthrough.Parser
    '''
    def test_parse_event(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'time_stamp': '2015-01-01T00:00:00',
        }
        parser = passthrough.Parser()
        parsed_event = parser.run(event)
        self.assertDictEqual(event, parsed_event)

    def test_parse_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no_pass',
            'time_stamp': '2015-01-01T00:00:00',
        }
        parser = passthrough.Parser()
        parsed_event = parser.run(event)
        self.assertIsNone(parsed_event)

# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.test_passthrough_parser
============================
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
        }
        parser = passthrough.Parser()
        parsed_event = parser.run(event)
        self.assertDictEqual(event, parsed_event)

    def test_parse_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no_pass',
        }
        parser = passthrough.Parser()
        parsed_event = parser.run(event)
        self.assertIsNone(parsed_event)

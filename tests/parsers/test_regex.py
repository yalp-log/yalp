# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.parsers.test_regex
=======================
'''
import unittest
from yalp.parsers import regex


class TestRegexParser(unittest.TestCase):
    '''
    Test the regex.Parser
    '''

    def test_parse_event(self):
        event = {
            'host': 'localhost',
            'message': 'Dec 10 an event',
            'time_stamp': '2015-01-01T00:00:00',
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertDictEqual(
            parsed_event,
            {
                'host': 'localhost',
                'month': 'Dec',
                'day': '10',
                'time_stamp': '2015-01-01T00:00:00',
            }
        )

    def test_parse_no_match(self):
        event = {
            'host': 'localhost',
            'message': 'Dec',
            'time_stamp': '2015-01-01T00:00:00',
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertDictEqual(event, parsed_event)

    def test_parse_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'Dec 10 an event',
            'type': 'not_regex',
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertDictEqual(event, parsed_event)

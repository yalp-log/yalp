# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.test_regex_parser
======================
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
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertDictEqual(
            parsed_event,
            {
                'host': 'localhost',
                'month': 'Dec',
                'day': '10',
            }
        )

    def test_parse_no_match(self):
        event = {
            'host': 'localhost',
            'message': 'Dec',
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertIsNone(parsed_event)

    def test_parse_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'Dec 10 an event',
            'type': 'not_regex',
        }
        parser = regex.Parser(regex=r'(?P<month>\w+)\s+(?P<day>\d+)')
        parsed_event = parser.run(event)
        self.assertIsNone(parsed_event)

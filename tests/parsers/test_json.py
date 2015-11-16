# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_json
=======================
'''
import unittest
from yalp.parsers import json


class TestJsonParser(unittest.TestCase):
    '''
    Test the json.Parser
    '''
    def test_parse_event(self):
        event = {
            'message': '{"key1": "value1", "key2": 2, "key3": "value3"}',
        }
        parser = json.Parser()
        parsed_event = parser.run(event)
        expected = {
            'key1': 'value1',
            'key2': 2,
            'key3': 'value3',
            'message': '{"key1": "value1", "key2": 2, "key3": "value3"}',
        }
        self.assertDictEqual(expected, parsed_event)

    def test_json_error(self):
        event = {
            'message': 'invalid: json,'
        }
        parser = json.Parser()
        parsed_event = parser.run(event)
        expected = {
            'message': 'invalid: json,'
        }
        self.assertDictEqual(expected, parsed_event)

    def test_empty_field(self):
        event = {
            'message': ''
        }
        parser = json.Parser()
        parsed_event = parser.run(event)
        expected = {
            'message': ''
        }
        self.assertDictEqual(expected, parsed_event)

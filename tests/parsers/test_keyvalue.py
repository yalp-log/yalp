# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_keyvalue
===========================
'''
import unittest
from yalp.parsers import keyvalue


class TestKeyValueParser(unittest.TestCase):
    '''
    Test the keyvalue.Parser
    '''
    def test_parse_event(self):
        event = {
            'message': 'key1:value1 key2:value2 key3:value3',
        }
        parser = keyvalue.Parser(field='message')
        parsed_event = parser.run(event)
        expected = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'message': 'key1:value1 key2:value2 key3:value3',
        }
        self.assertDictEqual(expected, parsed_event)

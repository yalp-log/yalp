# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_transform
============================
'''
import unittest
from yalp.parsers import transform


class TestTransformParser(unittest.TestCase):
    '''
    Test the transform.Parser
    '''
    def test_transsform_int(self):
        event = {
            'num_field': '200',
        }
        parser = transform.Parser(field='num_field', to='int')
        parsed_event = parser.run(event)
        self.assertIsInstance(parsed_event['num_field'], int)
        self.assertEqual(200, parsed_event['num_field'])

    def test_transsform_float(self):
        event = {
            'num_field': '200.01',
        }
        parser = transform.Parser(field='num_field', to='float')
        parsed_event = parser.run(event)
        self.assertIsInstance(parsed_event['num_field'], float)
        self.assertEqual(200.01, parsed_event['num_field'])

    def test_transsform_str(self):
        event = {
            'str_field': 200.01,
        }
        parser = transform.Parser(field='str_field', to='str')
        parsed_event = parser.run(event)
        self.assertIsInstance(parsed_event['str_field'], str)
        self.assertEqual('200.01', parsed_event['str_field'])

    def test_transform_error(self):
        event = {
            'str_field': 'abcd',
        }
        parser = transform.Parser(field='str_field', to='int')
        parsed_event = parser.run(event)
        self.assertIsInstance(parsed_event['str_field'], str)
        self.assertEqual('abcd', parsed_event['str_field'])

    def test_nested_int(self):
        event = {
            'nested': {
                'num_field': '200',
            }
        }
        parser = transform.Parser(field='nested:num_field', to='int')
        parsed_event = parser.run(event)
        self.assertIsInstance(parsed_event['nested']['num_field'], int)
        self.assertEqual(200, parsed_event['nested']['num_field'])

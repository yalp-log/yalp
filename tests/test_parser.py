# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_parser
=================
'''
import unittest
from nose.tools import raises

from yalp.parsers import tasks
from yalp.exceptions import ImproperlyConfigured


class TestParser(unittest.TestCase):
    '''
    Test parser
    '''
    def test_process_message(self):
        config = {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        }
        message = 'test message'
        parsed = tasks.process_message(config, message)
        self.assertEqual(parsed, message)

    @raises(ImproperlyConfigured)
    def test_process_message_invalid_config(self):
        config = {
            'module': 'yalp.parsers.plain',
        }
        message = 'test message'
        tasks.process_message(config, message)

    @raises(ImproperlyConfigured)
    def test_process_message_invalid_parser(self):
        config = {
            'module': 'bogus.module',
            'class': 'BogusClass',
        }
        message = 'test message'
        tasks.process_message(config, message)

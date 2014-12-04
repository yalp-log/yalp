# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_parser
=================
'''
import unittest
from nose.tools import raises

from yalp.config import settings
from yalp.parsers import tasks
from yalp.scripts import get_celery_app
from yalp.exceptions import ImproperlyConfigured


class TestParser(unittest.TestCase):
    '''
    Test parser
    '''
    def setUp(self):
        settings.celery_advanced = {
            'CELERY_ALWAYS_EAGER': True,
        }
        get_celery_app(settings)

    def test_process_message(self):
        settings.parers = [{
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        }]
        message = 'test message'
        parsed = tasks.process_message.delay(message)
        self.assertIn(message, parsed.result)

    @raises(ImproperlyConfigured)
    def test_process_message_invalid_config(self):
        settings.parsers = [{
            'module': 'yalp.parsers.plain',
        }]
        message = 'test message'
        tasks.process_message(message)

    @raises(ImproperlyConfigured)
    def test_process_message_invalid_parser(self):
        settings.parsers = [{
            'module': 'bogus.module',
            'class': 'BogusClass',
        }]
        message = 'test message'
        tasks.process_message(message)

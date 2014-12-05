# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_parser
=================
'''
from nose.tools import raises

from yalp.test import YalpTestCase
from yalp.test.utils import override_settings
from yalp.parsers import tasks
from yalp.exceptions import ImproperlyConfigured


class TestParser(YalpTestCase):
    '''
    Test parser
    '''
    @override_settings(parsers=[{
        'module': 'yalp.parsers.plain',
        'class': 'PlainParser',
    }])
    def test_process_message(self):
        ''' test processing a simple message '''
        event = {
            'message': 'test message'
        }
        parsed = tasks.process_message.delay(event)
        self.assertIn(event['message'], parsed.result)

    @override_settings(parsers=[{
        'module': 'yalp.parsers.plain',
        'class': 'PlainParser',
        'type_': 'test_type',
    }])
    def test_process_message_typed(self):
        ''' test processing a simple typed message '''
        event = {
            'message': 'test message',
            'type': 'test_type',
        }
        parsed = tasks.process_message.delay(event)
        print parsed.result
        self.assertIn(event['message'], parsed.result)

    @raises(ImproperlyConfigured)
    @override_settings(parsers=[{
        'module': 'yalp.parsers.plain',
    }])
    def test_invalid_config(self):
        ''' test raising exception on invalid config '''
        event = {
            'message': 'test message'
        }
        tasks.process_message(event)

    @raises(ImproperlyConfigured)
    @override_settings(parsers=[{
        'module': 'bogus.module',
        'class': 'BogusClass',
    }])
    def test_invalid_parser(self):
        ''' test raising exception on invalid parser module/class '''
        event = {
            'message': 'test message'
        }
        tasks.process_message(event)

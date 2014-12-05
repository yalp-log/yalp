# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_parser
=================
'''
from nose.tools import raises

from yalp.test import YalpTestCase, override_settings
from yalp.pipeline import tasks
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
        self.assertIn(event, parsed.result)

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
        self.assertIn(event, parsed.result)

    @override_settings(parsers=[
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        },
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        },
    ])
    def test_multi_parsers(self):
        ''' test processing a message with 2 parsers '''
        event = {
            'message': 'test message',
        }
        parsed = tasks.process_message.delay(event)
        self.assertEqual(len(parsed.result), 2)
        self.assertEqual(event, parsed.result[0])
        self.assertEqual(event, parsed.result[1])

    @override_settings(parsers=[
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
            'type': 'test_type',
        },
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        },
    ])
    def test_typed_multi_parsers(self):
        ''' test processing a typed message with 2 parsers '''
        event = {
            'message': 'test message',
            'type': 'test_type',
        }
        parsed = tasks.process_message.delay(event)
        self.assertIn(event, parsed.result)
        self.assertIn(None, parsed.result)

    @raises(ImproperlyConfigured)
    @override_settings(parsers=[{
        'module': 'yalp.parsers.plain',
    }])  # pylint: disable=R0201
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
    }])  # pylint: disable=R0201
    def test_invalid_parser(self):
        ''' test raising exception on invalid parser module/class '''
        event = {
            'message': 'test message'
        }
        tasks.process_message(event)

# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.core.test_parser_task
===========================
'''
from yalp.test import YalpTestCase

from yalp.pipeline import tasks


class TestParserTask(YalpTestCase):
    '''
    Test the process_message task
    '''
    _overridden_settings = {
        'parsers': [{
            'passthrough': {}
        }]
    }

    def test_process_message(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
        }
        result = tasks.process_message.apply(args=[event])
        self.assertEqual(event, result.result)

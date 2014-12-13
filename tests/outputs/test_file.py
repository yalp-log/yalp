# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.outputs.test_file
======================
'''
import unittest
import json

from yalp.outputs import file as file_outputer

try:
    from unittest.mock import patch
    BUILTIN = 'builtins'
except ImportError:
    BUILTIN = '__builtin__'
    from mock import patch


class TestFileOutput(unittest.TestCase):
    '''
    Test the file.Outputer
    '''
    @patch('{0}.open'.format(BUILTIN), create=True)
    def test_output_event(self, mock_open):
        event = {
            'host': 'localhost',
            'message': 'test message',
        }
        outputer = file_outputer.Outputer()
        outputer.run(event)
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.write.assert_called_with(json.dumps(event) + '\n')

    @patch('{0}.open'.format(BUILTIN), create=True)
    def test_output_event_skip_on_type(self, mock_open):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no out',
        }
        outputer = file_outputer.Outputer()
        outputer.run(event)
        file_handle = mock_open.return_value.__enter__.return_value
        self.assertFalse(file_handle.write.called)

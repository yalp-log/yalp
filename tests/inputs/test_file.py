# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.inputs.test_file
=====================
'''
import unittest
import time

from yalp.config import settings
from yalp.inputs import file as file_inputer

try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock


def _side_effect_function(path, *args):
    if path.startswith('/dev/null'):
        mocked_file = MagicMock()
        mocked_file.readline.side_effect = ['test message\n', None]
        return mocked_file
    else:
        return MagicMock()


class TestFileInput(unittest.TestCase):
    '''
    Test the file.Inputer
    '''
    def setUp(self):
        settings.home = '/tmp'
        self.inputer = file_inputer.Inputer('/dev/null')
        self.inputer.enqueue_event = MagicMock()

    @patch('yalp.inputs.file.open', create=True)
    def test_input_event(self, mock_open):
        mock_open.side_effect = _side_effect_function
        self.inputer.start()
        time.sleep(0.1)
        self.inputer.stop()
        self.inputer.join()
        mock_open.assert_any_call('/dev/null', 'r')
        self.inputer.enqueue_event.assert_called_with(
            {'message': 'test message'}
        )

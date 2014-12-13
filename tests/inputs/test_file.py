# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.inputs.test_file
=====================
'''
import unittest
import time

from yalp.inputs import file as file_inputer

try:
    from unittest.mock import patch, MagicMock
    BUILTIN = 'builtins'
except ImportError:
    BUILTIN = '__builtin__'
    from mock import patch, MagicMock


def _side_effect_function(path, *args):
    if path.startswith('mocked_path'):
        mocked_file = MagicMock()
        mocked_file.readline.return_value = 'test message'
        return mocked_file
    else:
        return MagicMock()


class TestFileInput(unittest.TestCase):
    '''
    Test the file.Inputer
    '''
    def setUp(self):
        self.inputer = file_inputer.Inputer('mocked_path')
        self.inputer.enqueue_event = MagicMock()

    @patch('{0}.open'.format('yalp.inputs.file'), create=True)
    def test_input_event(self, mock_open):
        mock_open.side_effect = _side_effect_function
        self.inputer.start()
        time.sleep(0.1)
        self.inputer.stop()
        self.inputer.join()
        mock_open.assert_any_call('mocked_path', 'r')
        self.inputer.enqueue_event.assert_called_with(
            {'message': 'test message'}
        )

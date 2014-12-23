# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_config
=================
'''
import unittest
import os

from yalp.config import load_config

try:
    from unittest.mock import patch
    BUILTIN = 'builtins'
except ImportError:
    from mock import patch
    BUILTIN = '__builtin__'



class TestConfig(unittest.TestCase):
    '''
    Test reading the config from a file.
    '''
    @patch('{0}.open'.format(BUILTIN), create=True)
    def test_load_config(self, mock_open):
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = (
            'parser_queue: mocked_parser_queue\n'
            'output_queue: mocked_output_queue\n'
        )
        opts = load_config('mock_config')
        self.assertEqual('mocked_parser_queue', opts['parser_queue'])
        self.assertEqual('mocked_output_queue', opts['output_queue'])

    @patch('{0}.open'.format(BUILTIN), create=True)
    def test_invalid_load_config(self, mock_open):
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = (
            'parser_queue: %mocked_parser_queue%\n'
            'output_queue: %mocked_output_queue%\n'
        )
        opts = load_config('mock_config')
        self.assertEqual('parsers', opts['parser_queue'])
        self.assertEqual('outputs', opts['output_queue'])

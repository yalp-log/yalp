# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_get_yalp_class
=========================
'''
import unittest
from yalp.utils import get_yalp_class


class TestGetYalpClass(unittest.TestCase):
    '''
    Test the get_yalp_class util function.
    '''
    def test_get_input_class(self):
        ''' test getting an input class '''
        plugin_type = 'input'
        plugin = 'file'
        config = {
            'path': '/dev/null',
        }
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.inputs.file import Inputer
        self.assertTrue(isinstance(instance, Inputer))

    def test_get_parser_class(self):
        ''' test getting an parser class '''
        plugin_type = 'parser'
        plugin = 'plain'
        config = {}
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.parsers.plain import Parser
        self.assertTrue(isinstance(instance, Parser))

    def test_get_output_class(self):
        ''' test getting an output class '''
        plugin_type = 'output'
        plugin = 'plain'
        config = {}
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.outputs.plain import Outputer
        self.assertTrue(isinstance(instance, Outputer))

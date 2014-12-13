# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_get_yalp_class
=========================
'''
import unittest
from nose.tools import raises
from yalp.utils import get_yalp_class
from yalp.exceptions import ImproperlyConfigured


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
        plugin = 'passthrough'
        config = {}
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.parsers.passthrough import Parser
        self.assertTrue(isinstance(instance, Parser))

    def test_get_output_class(self):
        ''' test getting an output class '''
        plugin_type = 'output'
        plugin = 'stdout'
        config = {}
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.outputs.stdout import Outputer
        self.assertTrue(isinstance(instance, Outputer))

    def test_get_parser_class_type(self):
        ''' test getting parser class with type '''
        plugin_type = 'parser'
        plugin = 'passthrough'
        config = {
            'type': 'passthrough',
        }
        instance = get_yalp_class(plugin, config, plugin_type)
        from yalp.parsers.passthrough import Parser
        self.assertTrue(isinstance(instance, Parser))
        self.assertEqual(instance.type_, 'passthrough')

    @raises(ImproperlyConfigured)
    def test_invalid_config(self):
        ''' test that exception is raised on no valid configs '''
        plugin_type = 'parser'
        plugin = 'no_such_plugin'
        config = {}
        get_yalp_class(plugin, config, plugin_type)

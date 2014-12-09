# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_inputsentrypoint
===========================
'''
import unittest
from yalp.scripts import InputsEntryPoint
from yalp.config import settings


class TestInputsEntryPointProperties(unittest.TestCase):
    '''
    Test properties on InputsEntryPoint
    '''
    def setUp(self):
        settings.inputs = []

    def tearDown(self):
        settings.inputs = []

    def test_inputers_property(self):
        ''' test getting inputers via property '''
        settings.inputs = [{
            'file': {
                'path': '/dev/null'
            }
        }]
        entrypoint = InputsEntryPoint()
        inputers = entrypoint.inputers
        from yalp.inputs.file import Inputer
        self.assertEqual(len(inputers), 1)
        for inputer in inputers:
            self.assertIsInstance(inputer, Inputer)

    def test_multi_inputers(self):
        ''' test getting multiple inputers via property '''
        settings.inputs = [
            {
                'file': {
                    'path': '/dev/null'
                }
            },
            {
                'file': {
                    'path': '/dev/zero',
                }
            },
        ]
        entrypoint = InputsEntryPoint()
        inputers = entrypoint.inputers
        self.assertEqual(len(inputers), 2)
        from yalp.inputs.file import Inputer
        for inputer in inputers:
            self.assertIsInstance(inputer, Inputer)

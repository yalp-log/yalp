# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.test_version
==================
'''
import unittest


class TestVersion(unittest.TestCase):
    '''
    Test getting version
    '''
    def test_get_version(self):
        from yalp import version
        self.assertIsNotNone(version.__version__)

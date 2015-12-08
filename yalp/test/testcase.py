# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.test.testcase
==================
'''

import sys
import unittest
from ..config import settings
from ..pipeline.tasks import app

from .utils import override_settings


class YalpTestCase(unittest.TestCase):
    '''
    Base Yalp Test case. Handles settings up settings and allowing for
    easily overriding.
    '''
    _overridden_settings = None

    @classmethod
    def setUpClass(cls):
        if cls._overridden_settings:
            cls._cls_overridden_context = override_settings(
                **cls._overridden_settings)  # pylint: disable=not-a-mapping
            cls._cls_overridden_context.enable()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, '_cls_overridden_context'):
            cls._cls_overridden_context.disable()
            delattr(cls, '_cls_overridden_context')

    def __call__(self, result=None, **kwargs):
        '''
        Wrapper around default __call__ method to perform common Yalp test
        set up. This means that user-defined Test Cases aren't required to
        include a call to super().setUp().
        '''
        testMethod = getattr(             # pylint: disable=C0103
            self, self._testMethodName)
        skipped = (getattr(self.__class__, "__unittest_skip__", False) or
                   getattr(testMethod, "__unittest_skip__", False))

        if not skipped:
            try:
                self._pre_setup()
            except Exception:  # pylint: disable=W0703
                result.addError(self, sys.exc_info())
                return
        super(YalpTestCase, self).__call__(result)
        if not skipped:
            try:
                self._post_teardown()
            except Exception:  # pylint: disable=W0703
                result.addError(self, sys.exc_info())
                return

    def _pre_setup(self):
        '''
        Performs any pre-test setup. Setting CELERY_ALWAYS_EAGER and
        getting the celery app with the current settings.
        '''
        settings.celery_advanced = {
            'CELERY_ALWAYS_EAGER': True,
        }
        self.app = app

    def _post_teardown(self):
        '''
        Performs any post-test things.
        '''
        pass

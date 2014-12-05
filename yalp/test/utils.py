# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.test.utils
===============
'''
from functools import wraps
from ..config import settings, UserSettingsHolder


# pylint: disable=W0212
class override_settings(object):  # pylint: disable=C0103
    '''
    Acts as either a decorator, or a context manager. If it's a decorator it
    takes a function and returns a wrapped function. If it's a contextmanager
    it's used with the ``with`` statement. In either event entering/exiting
    are called before and after, respectively, the function/block is executed.
    '''
    def __init__(self, **kwargs):
        self.options = kwargs

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        from .testcase import YalpTestCase
        if isinstance(test_func, type):
            if not issubclass(test_func, YalpTestCase):
                raise Exception(
                    'Only subclasses of YalpTestCase can be decorated '
                    'with override_settings')
            self.save_options(test_func)
            return test_func
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):  # pylint: disable=C0111
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def save_options(self, test_func):  # pylint: disable=C0111
        if test_func._overridden_settings is None:
            test_func._overridden_settings = self.options
        else:
            # Duplicate dict to prevent subclasses from altering their parent.
            test_func._overridden_settings = dict(
                test_func._overridden_settings, **self.options)

    def enable(self):
        ''' Enable overrides to settings.  '''
        override = UserSettingsHolder(settings._wrapped)
        for key, new_value in self.options.items():
            setattr(override, key, new_value)
        self.wrapped = settings._wrapped
        settings._wrapped = override

    def disable(self):
        ''' Disable overrides to settings. '''
        settings._wrapped = self.wrapped
        del self.wrapped
# pylint: enable=W0212

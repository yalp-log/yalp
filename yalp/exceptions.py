# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.exceptions
===============
'''


class ImproperlyConfigured(Exception):
    '''
    Raised when configuration is not correct.
    '''


class ShutdownException(Exception):
    '''
    Raised when sigterm is sent to shutdown.
    '''


class OutputException(Exception):
    '''
    Raised when something is invalid when attempting to output an event.
    '''

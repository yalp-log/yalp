# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs
============
'''
import logging

logger = logging.getLogger(__name__)


class BaseOutputer(object):
    '''
    Base outputer.
    '''

    def __init__(self, config):
        self.config = config

    def output(self, event):
        '''
        Parse the log message.
        '''
        logger.info(event)

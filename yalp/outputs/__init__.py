# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs
============
'''
from .. import BaseYalp

import logging
logger = logging.getLogger(__name__)


class BaseOutputer(BaseYalp):
    '''
    Base outputer.
    '''
    def run(self, event):
        '''
        Parse the log message.
        '''
        if self.type_ != event.get('type', None):
            logger.info('%s skipping event %s: not same type',
                        self.__class__.__name__,
                        event)
        else:
            self.output(event)

    def output(self, event):
        '''
        Output the event.
        '''
        raise NotImplementedError

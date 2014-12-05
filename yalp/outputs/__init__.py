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
    def __init__(self, type_=None, **kwargs):  # pylint: disable=W0613
        self.type_ = type_

    def output(self, event):
        '''
        Parse the log message.
        '''
        if self.type_ != event.get('type', None):
            logger.info('%s skipping event %s: not same type',
                        self.__class__.__name__,
                        event)
        else:
            logger.info(event)

# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''
from .. import BaseYalp

import logging
logger = logging.getLogger(__name__)


class BaseParser(BaseYalp):
    '''
    Base parser.
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
            parsed_event = self.parse(event)
            from yalp.pipeline import tasks
            tasks.process_output.delay(parsed_event)
            return event['message']

    def parse(self, event):
        '''
        Parse the message and return event with parsed result.
        '''
        raise NotImplementedError

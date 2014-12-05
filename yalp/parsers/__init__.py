# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''
from ..pipeline import CeleryPipeline

import logging
logger = logging.getLogger(__name__)


class BaseParser(CeleryPipeline):
    '''
    Base parser.
    '''
    def __init__(self, *args, **kwargs):
        super(BaseParser, self).__init__(*args, **kwargs)

    def process_event(self, event):
        parsed_event = self.parse(event)
        from yalp.pipeline import tasks
        tasks.process_output.delay(parsed_event)
        return event['message']

    def parse(self, event):
        '''
        Parse the message and return event with parsed result.
        '''
        raise NotImplementedError

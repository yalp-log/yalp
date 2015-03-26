# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''
import logging
from ..pipeline import CeleryPipeline


class BaseParser(CeleryPipeline):
    '''
    Base parser.
    '''
    def __init__(self, *args, **kwargs):
        super(BaseParser, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def process_event(self, event):
        return self.parse(event)

    def parse(self, event):
        '''
        Parse the message and return event with parsed result.
        '''
        raise NotImplementedError

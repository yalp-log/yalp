# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''
import logging

from ..utils import nested_get
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


class ExtractFieldParser(BaseParser):
    '''
    Extracts a field from the event for parsing.

    If the field is not in the event, the event is not parsed.
    '''
    def __init__(self, field='message', *args, **kwargs):
        super(ExtractFieldParser, self).__init__(*args, **kwargs)
        self.field = field

    def process_event(self, event):
        try:
            self.data = nested_get(event, self.field)
            return super(ExtractFieldParser, self).process_event(event)
        except KeyError:
            return event

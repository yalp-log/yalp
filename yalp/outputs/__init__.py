# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs
============
'''
from ..pipeline import CeleryPipeline

import logging
logger = logging.getLogger(__name__)


class BaseOutputer(CeleryPipeline):
    '''
    Base outputer.
    '''
    def __init__(self, *args, **kwargs):
        super(BaseOutputer, self).__init__(*args, **kwargs)

    def process_event(self, event):
        return self.output(event)

    def output(self, event):
        '''
        Output the event.
        '''
        raise NotImplementedError

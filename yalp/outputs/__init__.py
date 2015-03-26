# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs
============
'''
import logging
from ..pipeline import CeleryPipeline


class BaseOutputer(CeleryPipeline):
    '''
    Base outputer.
    '''
    def __init__(self, *args, **kwargs):
        super(BaseOutputer, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def process_event(self, event):
        return self.output(event)

    def output(self, event):
        '''
        Output the event.
        '''
        raise NotImplementedError

    def shutdown(self):
        '''
        Shutdown the outputer, closing resources.
        '''
        raise NotImplementedError

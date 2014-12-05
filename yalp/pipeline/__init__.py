# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline
=============
'''
from threading import Thread

import logging
logger = logging.getLogger(__name__)


class BasePipline(object):
    '''
    Base yalp class.
    '''
    def __init__(self, type_=None, **kwargs):  # pylint: disable=W0613
        super(BasePipline, self).__init__()
        self.type_ = type_


class CeleryPipeline(BasePipline):
    '''
    Pipeline class that iteracts with celery.
    '''
    def __init__(self, **kwargs):
        super(CeleryPipeline, self).__init__(**kwargs)

    def run(self, event):
        '''
        Execute this pipeline component with the event.
        '''
        if self.type_ != event.get('type', None):
            logger.info('%s skipping event %s: not same type',
                        self.__class__.__name__,
                        event)
        else:
            return self.process_event(event)

    def process_event(self, event):
        '''
        Process the event.
        '''
        raise NotImplementedError


class ThreadPipline(BasePipline, Thread):
    '''
    Pileline class that is used by threads.
    '''
    def __init__(self, *args, **kwargs):
        super(ThreadPipline, self).__init__(*args, **kwargs)

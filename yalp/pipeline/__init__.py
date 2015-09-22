# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline
=============
'''
import threading
import logging


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
        self.logger = logging.getLogger(__name__)

    def run(self, event):
        '''
        Execute this pipeline component with the event.
        '''
        if event is None or self.type_ != event.get('type', None):
            self.logger.info('%s skipping event %s: not same type',
                             self.__class__.__name__,
                             event)
            return event
        else:
            self.logger.info('processing event %s', event)
            return self.process_event(event)

    def process_event(self, event):
        '''
        Process the event.
        '''
        raise NotImplementedError


class ThreadPipline(BasePipline, threading.Thread):
    '''
    Pileline class that is used by threads.
    '''
    def __init__(self, *args, **kwargs):
        super(ThreadPipline, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()

    def stop(self):
        ''' Inform the thread to stop '''
        self._stopper.set()

    @property
    def stopped(self):
        ''' True if thread has been told to stop '''
        return self._stopper.is_set()

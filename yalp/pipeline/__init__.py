# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline
=============
'''
import threading
import logging

from .filters import FILTER_MAP


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
    def __init__(self, filters=None, **kwargs):
        super(CeleryPipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.filters = filters
        if self.type_:
            self.logger.warn('Using DEPRECATED type field. Use filters instead')
            type_filter = [['type', self.type_]]
            filter_type = 'field_equals'
        else:
            type_filter = ['type']
            filter_type = 'not_has_fields'
        try:
            self.filters[filter_type].extend(type_filter)
        except KeyError:
            self.filters[filter_type] = type_filter
        except TypeError:
            self.filters = {filter_type: type_filter}

    def pass_filters(self, event):
        '''
        Check if the event passes the filters.
        '''
        if self.filters is None:
            return True
        for filter_type, filter_ in self.filters.items():
            if filter_type in FILTER_MAP:
                if FILTER_MAP[filter_type](filter_, event):
                    return True
            else:
                self.logger.warn('Invalid filter type: %s', filter_type)
        return False

    def run(self, event):
        '''
        Execute this pipeline component with the event.
        '''
        if self.pass_filters(event):
            return self.process_event(event)
        else:
            return event

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

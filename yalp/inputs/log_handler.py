# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.log_handler
=======================
'''
from __future__ import absolute_import

import time
import logging

from ..config import settings
from ..utils import get_hostname

from . import InputerMixin, DEFAULT_DATE_FMT

RESEVERD = frozenset((
    'stack',
    'args',
    'name',
    'msg',
    'message',
    'exc_info',
    'created',
    'msecs',
    'relativeCreated',
    'tags',
))


class Inputer(logging.Handler, InputerMixin, object):
    '''
    Get input from python logging
    '''
    convert = time.localtime

    def __init__(self,
                 pipeline=None,
                 *args,
                 **kwargs):  # pylint: disable=unused-argument
        pipeline = pipeline or {}
        self.parsers = pipeline.pop('parsers', False)
        settings.update(pipeline)
        self.type_ = kwargs.get('type')
        self.hostname = get_hostname()
        logging.Handler.__init__(
            self,
            level=kwargs.get('level', logging.NOTSET),
        )

    def _timestamp(self, created):
        ''' Convert created time to time_stamp '''
        converted_time = self.convert(created)
        return time.strftime(DEFAULT_DATE_FMT, converted_time)

    def emit(self, record):
        event = {}
        for key, val in vars(record).iteritems():
            if key.startswith('_') or key in RESEVERD:
                continue
            event[key] = val

        event.update({
            'time_stamp': self._timestamp(record.created),
            'message': self.format(record),
            'logger': record.name,
        })

        self.enqueue_event(event)

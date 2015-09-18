# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.log_handler
=======================

The log handler inputer is for use within Python's `logging facility`_.
Therefore it uses a different configuration method than normal YALP
plugins. Instead of using the YALP `YAML` configuration file, this
inputer is configured in another project's python logging configuration.

For example, in another Python project:

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disabled_existing_loggers': False,
        'handlers': {
            'yalp': {
                'level': 'INFO',
                'class': 'yalp.inputs.log_handler.YalpHandler',
                'type': 'my_package_logs',
                'pipeline': {
                    'broker_url': 'amqp://guest@guest@localhost:5672//',
                },
            },
        },
        'loggers': {
            'my_package': {
                'handlers': ['yalp']
                'level': 'INFO',
            },
        }
    }

The handler accepts the following optional fields:

*type*
    The type of the event for the parsers/outputers to filter on.

*pipeline*
    A dictionary of YALP configuration settings. The ``pipeline`` option
    accepts the following fields:

    *parsers*
        Boolean option. If true events will be sent to the parsers, otherwise
        they will be sent directly to the outputers. Default is ``False``.

    Additionaly, ``pipeline`` option for the handler accepts all of the YALP
    Celery :ref:`configuration` settings, such as the ``broker_url``, with
    the same defaults.


Then in the Python project, send a log message as follows:

.. code-block:: python

    logger.info('a log message', extra={'additional': 'data will be included'})

This will create an event like:

.. code-block:: python

    {
        'time_stamp': '2015-01-01T01:00:00',
        'message': 'a log message',
        'additional': 'data will be included',
        'logger': 'my_pacakge.my_module',
        'funcName': 'func_with_log',
        'levelname': 'INFO',
        'levelno': 20,
        'hostname': 'my_host',
    }

.. _logging facility: https://docs.python.org/3/library/logging.html
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


class YalpHandler(logging.Handler, InputerMixin, object):
    '''
    Get input from python logging
    '''
    convert = time.gmtime

    def __init__(self,
                 pipeline=None,
                 *args,
                 **kwargs):  # pylint: disable=unused-argument
        pipeline = pipeline or {}
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
        for key, val in vars(record).items():
            if key.startswith('_') or key in RESEVERD:
                continue
            event[key] = val

        event.update({
            'time_stamp': self._timestamp(record.created),
            'message': self.format(record),
            'logger': record.name,
        })

        self.enqueue_event(event)


Inputer = YalpHandler

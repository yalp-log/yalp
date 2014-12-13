# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.scripts
============
'''
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import time
import argparse

import logging
logger = logging.getLogger(__name__)

from . import version
from .config import settings
from .utils import get_yalp_class, get_hostname
from .pipeline.tasks import app
from .exceptions import ShutdownException


class BaseEntryPoint(object):
    '''
    Main Entry point.
    '''
    def __init__(self,
                 description=None,
                 argv=None,
                 *args,
                 **kwargs):  # pylint: disable=W0613
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.description = description or self.prog_name
        self.parser = argparse.ArgumentParser(description='YALP')

    def add_arguments(self):
        '''
        Add arguments to arg parser.
        '''
        self.parser.add_argument('-v', '--version',
                                 action='store_true',
                                 default=False,
                                 help='Display YALP version')
        self.parser.add_argument('-c', '--config',
                                 default=None,
                                 help='Specify alternative config')

    def execute(self):
        '''
        Execute command.
        '''
        self.add_arguments()
        self.options = self.parser.parse_args(self.argv[1:])
        if self.options.version:
            print(version.__version__)
            sys.exit(0)
        if self.options.config:
            os.environ['YALP_CONFIG_FILE'] = self.options.config
        self.app = app


class ParsersEntryPoint(BaseEntryPoint):
    '''
    Entry point for starting parser workers.
    '''
    def execute(self):
        super(ParsersEntryPoint, self).execute()
        self.app.worker_main([
            'yalp-parsers',
            '--concurrency={0}'.format(settings.parser_workers),
            '--queues={0}'.format(settings.parser_queue),
            '--hostname={0}-{1}'.format(
                get_hostname(),
                settings.parser_worker_name,
            )
        ])


class OutputersEntryPoint(BaseEntryPoint):
    '''
    Entry point for starting outputers workers.
    '''
    def execute(self):
        super(OutputersEntryPoint, self).execute()
        self.app.worker_main([
            'yalp-outputers',
            '--concurrency={0}'.format(settings.output_workers),
            '--queues={0}'.format(settings.output_queue),
            '--hostname={0}-{1}'.format(
                get_hostname(),
                settings.output_worker_name,
            )
        ])


def sigterm_handler(signo, stack_frame):  # pylint: disable=W0613
    '''
    Catch signal and raise ShutdownException to preform cleanup.
    '''
    raise ShutdownException(signo)


class InputsEntryPoint(BaseEntryPoint):
    '''
    Entry point for starting inputers.
    '''
    _inputers = None

    def __init__(self, max_iterations=None, interval=1, *args, **kwargs):
        super(InputsEntryPoint, self).__init__(*args, **kwargs)
        self.max_iterations = max_iterations
        self.interval = interval

    @property
    def inputers(self):
        '''
        Get the list of inputer classes.
        '''
        if self._inputers is None:
            inputers = []
            for conf in settings.inputs:
                for plugin, config in conf.items():
                    inputers.append(get_yalp_class(plugin, config, 'input'))
            self._inputers = inputers
        return self._inputers

    def check_iterations(self):
        ''' Check if we should sleep again '''
        if self.max_iterations is not None:
            self.max_iterations -= 1
            if self.max_iterations <= 0:
                raise ShutdownException
        return True

    def execute(self):
        super(InputsEntryPoint, self).execute()
        import signal
        signal.signal(signal.SIGTERM, sigterm_handler)
        signal.signal(signal.SIGINT, sigterm_handler)
        try:
            for inputer in self.inputers:
                inputer.start()
            while self.check_iterations():
                time.sleep(self.interval)
        except ShutdownException:
            for inputer in self.inputers:
                inputer.stop()
            for inputer in self.inputers:
                inputer.join()


class CliEntryPoint(BaseEntryPoint):
    '''
    Entry point for cli.
    '''
    def add_arguments(self):
        super(CliEntryPoint, self).add_arguments()
        self.parser.add_argument('-t', '--type',
                                 default=None,
                                 help='Specify message type')
        self.parser.add_argument('message',
                                 metavar='message',
                                 type=str,
                                 nargs='?',
                                 default='test message',
                                 help='Message to process')

    def execute(self):
        super(CliEntryPoint, self).execute()
        event = {
            'message': self.options.message,
            'type': self.options.type,
        }
        from yalp.pipeline import tasks
        if settings.parsers:
            tasks.process_message.delay(event)
        else:
            tasks.process_output.delay(event)

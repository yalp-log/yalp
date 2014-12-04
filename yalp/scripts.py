# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.scripts
============
'''
from celery import Celery

import logging
logger = logging.getLogger(__name__)

from .config import load_config


def _get_hostname():
    '''
    Get system's hostname for worker process name.
    '''
    import socket
    hostname = socket.gethostname()
    del socket
    return hostname


def get_celery_app(config):
    '''
    Create the parsers celery app.
    '''
    app = Celery()
    app.conf.update(
        BROKER_URL=config['broker_url'],
        CELERY_ROUTES={
            'yalp.parsers.tasks.process_message': {
                'queue': config['parser_queue'],
            },
            'yalp.outputs.tasks.process_output': {
                'queue': config['output_queue'],
            },
        },
    )
    app.autodiscover_tasks(lambda: (
        'yalp.parsers',
        'yalp.outputs',
    ))
    return app


class BaseEntryPoint(object):
    '''
    Common entry point code.
    '''
    def __init__(self, config_path=None):
        self.config = load_config(config_path)
        self.app = get_celery_app(self.config)


class ParsersEntryPoint(BaseEntryPoint):
    '''
    Entry point for starting parser workers.
    '''
    def __init__(self, config_path=None):
        super(ParsersEntryPoint, self).__init__(config_path=config_path)
        self.app.worker_main([
            'yalp-parsers',
            '--concurrency={0}'.format(self.config['parser_workers']),
            '--queues={0}'.format(self.config['parser_queue']),
            '--hostname={0}-{1}'.format(
                _get_hostname(),
                self.config['parser_worker_name'],
            )
        ])


class OutputersEntryPoint(BaseEntryPoint):
    '''
    Entry point for starting outputers workers.
    '''
    def __init__(self, config_path=None):
        super(OutputersEntryPoint, self).__init__(config_path=config_path)
        self.app.worker_main([
            'yalp-outputers',
            '--concurrency={0}'.format(self.config['output_workers']),
            '--queues={0}'.format(self.config['output_queue']),
            '--hostname={0}-{1}'.format(
                _get_hostname(),
                self.config['output_worker_name'],
            )
        ])


class CliEntryPoint(BaseEntryPoint):
    '''
    Entry point for cli.
    '''
    def __init__(self, config_path=None, message='test message'):
        super(CliEntryPoint, self).__init__(config_path=config_path)
        from yalp.parsers import tasks
        tasks.process_message.delay(message)

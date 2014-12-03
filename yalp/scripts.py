# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.scripts
============
'''
from celery import Celery
from kombu import Exchange, Queue

import logging
logger = logging.getLogger(__name__)


def get_parsers_app():
    '''
    Create the parsers celery app.
    '''
    parsers_app = Celery()
    parsers_app.conf.update(
        BROKER_URL='amqp://guest:guest@localhost:5672//',
        CELERY_ROUTES={
            'yalp.parsers.tasks.process_message': {'queue': 'parse'},
            'yalp.outputs.tasks.process_output': {'queue': 'outputs'},
        },
    )
    parsers_app.autodiscover_tasks(lambda: ('yalp.parsers',))
    return parsers_app


def get_outputers_app():
    '''
    Create the outputers celery app.
    '''
    outputers_app = Celery()
    outputers_app.conf.update(
        BROKER_URL='amqp://guest:guest@localhost:5672//',
        CELERY_ROUTES={
            'yalp.parsers.tasks.process_message': {'queue': 'parse'},
            'yalp.outputs.tasks.process_output': {'queue': 'outputs'},
        },
    )
    outputers_app.autodiscover_tasks(lambda: ('yalp.outputs',))
    return outputers_app


def parsers_main():
    '''
    Entry point for starting parser workers.
    '''
    parsers_app = get_parsers_app()
    parsers_app.worker_main([
        'yalp-parsers',
        '--queues=parse',
        '--hostname=parser-workers',
    ])


def outputers_main():
    '''
    Entry point for starting outputers workers.
    '''
    outputers_app = get_outputers_app()
    outputers_app.worker_main([
        'yalp-outputers',
        '--queues=outputs',
        '--hostname=output-workers',
    ])


def cli_main(message='test message'):
    '''
    Entry point for cli.
    '''
    get_parsers_app()
    config = {
        'module': 'yalp.parsers.plain',
        'class': 'PlainParser',
        'outputs': [
            {
                'module': 'yalp.outputs.plain',
                'class': 'PlainOutputer',
            },
        ],
    }
    from yalp.parsers import tasks
    tasks.process_message.delay(config, message)

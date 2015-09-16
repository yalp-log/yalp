# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline.tasks
===================
'''
from __future__ import absolute_import
from celery import Celery, Task, bootsteps, uuid
from kombu import Consumer, Exchange, Queue

from ..config import settings
from ..utils import get_yalp_class


class YalpOutputersConsumer(bootsteps.ConsumerStep):
    '''
    Yalp outputer consumer
    '''
    _config = None
    _outputers = None

    @property
    def config(self):
        '''
        Get the configuration.
        '''
        if self._config is None:
            self._config = settings
        return self._config

    @property
    def outputers(self):
        '''
        Get the list of output classes.
        '''
        if self._outputers is None:
            outputs = []
            for conf in self.config.outputs:
                for plugin, config in conf.items():
                    outputs.append(get_yalp_class(plugin, config, 'output'))
            self._outputers = outputs
        return self._outputers

    def get_consumers(self, channel):
        return [
            Consumer(
                channel,
                queues=[Queue(settings.output_queue,
                              Exchange(settings.output_queue),
                              settings.output_queue)],
                callbacks=[self.handle_message],
                accept=['pickle', 'json', 'msgpack', 'yaml'],
            )
        ]

    def handle_message(self, body, message):
        '''
        Process the message.
        '''
        for outputer in self.outputers:
            outputer.run(body['message'])
        message.ack()

    def shutdown(self, c):
        for outputer in self.outputers:
            outputer.shutdown()
        super(YalpOutputersConsumer, self).shutdown(c)


def lazy_update_app_config():
    '''
    Load settings into celery as late as possible.
    '''
    config_updates = {
        'BROKER_URL': settings.broker_url,
        'CELERY_ROUTES': {
            'yalp.pipeline.tasks.process_message': {
                'queue': settings.parser_queue,
            },
        },
    }
    config_updates.update(settings.celery_advanced)
    return config_updates


app = Celery()
app.add_defaults(lazy_update_app_config)


class PipelineTask(Task):
    '''
    Pipeline celery task.
    '''
    abstract = True
    _config = None
    _parsers = None
    _outputers = None
    _output_queue = None
    _output_exchange = None

    @property
    def config(self):
        '''
        Get the parsers configuration.
        '''
        if self._config is None:
            self._config = settings
        return self._config

    @property
    def parsers(self):
        '''
        Get the list of parser classes.
        '''
        if self._parsers is None:
            parsers = []
            for conf in self.config.parsers:
                for plugin, config in conf.items():
                    parsers.append(get_yalp_class(plugin, config, 'parser'))
            self._parsers = parsers
        return self._parsers

    def reload_config(self):
        '''
        Re-read config from settings
        '''
        self._config = None
        self._parsers = None


def process_output(event):
    '''
    Send the event to the output consumer.
    '''
    exchange = Exchange(settings.output_queue)
    queue = Queue(settings.output_queue,
                  exchange,
                  settings.output_queue)
    with app.producer_or_acquire(None) as producer:
        producer.publish(
            {
                'task': 'yalp.pipeline.process_output',
                'id': uuid(),
                'message': event
            },
            serializer=settings.celery_serializer,
            exchange=exchange,
            routing_key=settings.output_queue,
            declare=[queue],
            retry=True,
        )


@app.task(base=PipelineTask)
def process_message(event):
    '''
    Process a message using settings from config.

    event
        The event to process. A dict containing the message. For example:

        .. code-block:: python

            {
                'message': 'the message to parse',
                'time_stamp': '2015-01-01T01:00:00',
                'hostname': 'input_host',
            }
    '''
    for parser in process_message.parsers:
        event = parser.run(event)
    process_output(event)
    return event

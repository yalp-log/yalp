# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline.tasks
===================
'''
from __future__ import absolute_import
from celery import Celery, Task

from ..config import settings
from ..utils import get_yalp_class


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
            'yalp.pipeline.tasks.process_output': {
                'queue': settings.output_queue,
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


@app.task(base=PipelineTask)
def process_message(event):
    '''
    Process a message using settings from config.

    message
        The message to process, generally a string.
    '''
    parsed_events = [parser.run(event) for parser in process_message.parsers]
    for parsed_event in parsed_events:
        if parsed_event:
            process_output.delay(parsed_event)
    return parsed_events


@app.task(base=PipelineTask)
def process_output(event):
    '''
    Output events
    '''
    return [outputer.run(event) for outputer in process_output.outputers]

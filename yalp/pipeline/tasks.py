# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline.tasks
===================
'''
from celery import shared_task, Task

from ..config import settings
from ..utils import get_yalp_class


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
            self._parsers = [
                get_yalp_class(**conf) for conf in self.config.parsers]
        return self._parsers

    @property
    def outputers(self):
        '''
        Get the list of output classes.
        '''
        if self._outputers is None:
            self._outputers = [
                get_yalp_class(**conf) for conf in self.config.outputs]
        return self._outputers


@shared_task(base=PipelineTask)
def process_message(event):
    '''
    Process a message using settings from config.

    message
        The message to process, generally a string.
    '''
    print 'in process_message'
    return [parser.run(event) for parser in process_message.parsers]


@shared_task(base=PipelineTask)
def process_output(event):
    '''
    Output events
    '''
    return [outputer.run(event) for outputer in process_output.outputers]

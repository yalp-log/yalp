# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.tasks
==================
'''
from celery import shared_task, Task

from ..config import settings
from ..utils import get_yalp_class


class ParserTask(Task):
    '''
    Parser celery task.
    '''
    abstract = True
    _config = None
    _parsers = None

    @property
    def config(self):
        '''
        Get the parsers configuration.
        '''
        if self._config is None:
            self._config = settings.parsers
        return self._config

    @property
    def parsers(self):
        '''
        Get the list of parser classes.
        '''
        if self._parsers is None:
            self._parsers = [get_yalp_class(**conf) for conf in self.config]
        return self._parsers


@shared_task(base=ParserTask)
def process_message(event):
    '''
    Process a message using settings from config.

    message
        The message to process, generally a string.
    '''
    ret = [parser.run(event) for parser in process_message.parsers]
    return ret

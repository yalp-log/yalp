# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.tasks
==================
'''
from celery import shared_task, Task

from ..config import settings
from ..utils import get_yalp_class


class OutputTask(Task):
    '''
    Output celery task.
    '''
    abstract = True
    _config = None
    _outputers = None

    @property
    def config(self):
        '''
        Get the outputs configuration.
        '''
        if self._config is None:
            self._config = settings.outputs
        return self._config

    @property
    def outputers(self):
        '''
        Get the list of output classes.
        '''
        if self._outputers is None:
            self._outputers = [get_yalp_class(**conf) for conf in self.config]
        return self._outputers


@shared_task(base=OutputTask)
def process_output(event):
    '''
    Output events
    '''
    ret = [outputer.run(event) for outputer in process_output.outputers]
    return ret

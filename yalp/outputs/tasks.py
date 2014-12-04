# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.tasks
==================
'''
from celery import shared_task, Task

from ..config import load_output_config
from ..exceptions import ImproperlyConfigured


def _get_outputer(**config):
    '''
    Get the outputer class from the config
    '''
    try:
        outputer_module_name = config['module']
        outputer_class_name = config['class']
        outputer_module = __import__(outputer_module_name,
                                     fromlist=[outputer_class_name])
        outputer_class = getattr(outputer_module, outputer_class_name)
        return outputer_class(**config)
    except KeyError:
        raise ImproperlyConfigured('Invalid config.')
    except ImportError:
        raise ImproperlyConfigured('Invalid outputer module/class.')


class OutputTask(Task):
    abstract = True
    _config = None
    _outputers = None

    @property
    def config(self):
        if self._config is None:
            self._config = load_output_config(None)
        return self._config

    @property
    def outputers(self):
        if self._outputers is None:
            self._outputers = [_get_outputer(**conf) for conf in self.config]
        return self._outputers


@shared_task(base=OutputTask)
def process_output(event):
    '''
    Output events
    '''
    for outputer in process_output.outputers:
        outputer.output(event)

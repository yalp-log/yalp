# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.tasks
==================
'''
from celery import shared_task, Task

from ..config import settings
from ..exceptions import ImproperlyConfigured


def _get_parser(**config):
    '''
    Get the parser class from the config
    '''
    try:
        parser_module_name = config['module']
        parser_class_name = config['class']
        parser_module = __import__(parser_module_name,
                                   fromlist=[parser_class_name])
        parser_class = getattr(parser_module, parser_class_name)
        return parser_class(**config)
    except KeyError:
        raise ImproperlyConfigured('Invalid config.')
    except ImportError:
        raise ImproperlyConfigured('Invalid parser module/class.')


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
            self._parsers = [_get_parser(**conf) for conf in self.config]
        return self._parsers


@shared_task(base=ParserTask)
def process_message(message):
    '''
    Process a message using settings from config.

    message
        The message to process, generally a string.
    '''
    ret = []
    for parser in process_message.parsers:
        ret.append(parser.parse(message))
    return ret

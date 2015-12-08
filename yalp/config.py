# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.config
===========
'''
from __future__ import print_function

import os
from logging.config import dictConfig
import yaml


EMPTY = object()

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'yalp.inputs': {
            'handlers': ['console'],
        },
        'yalp.parsers': {
            'handlers': ['console'],
        },
        'yalp.outputs': {
            'handlers': ['console'],
        },
    }
}

DEFAULT_OPTS = {
    'broker_url': 'amqp://guest:guest@localhost:5672//',
    'parser_queue': 'parsers',
    'output_queue': 'outputs',
    'parser_worker_name': 'parser-workers',
    'output_worker_name': 'output-workers',
    'parser_workers': 5,
    'output_workers': 1,
    'celery_advanced': {},
    'celery_serializer': 'pickle',
    'inputs': [],
    'parsers': [],
    'outputs': [],
    'home': None,
    'input_packages': ['yalp.inputs'],
    'parser_packages': ['yalp.parsers'],
    'output_packages': ['yalp.outputs'],
    'log_format': '%(name)s: %(levelname)s [%(module)s:%(lineno)s] %(message)s',
    'log_level': 'WARN',
    'logging': None,
}


def _read_conf_file(path):
    '''
    Parse yaml config file into dictionary.
    '''
    if path is None:
        return {}

    with open(path, 'r') as conf_file:
        try:
            conf_opts = yaml.safe_load(conf_file.read()) or {}
        except yaml.YAMLError as err:
            print('Error parsing configuration file: %s - %s' % (path, err))
            conf_opts = {}
        return conf_opts


def load_config(path, defaults=None):
    '''
    Read in config file.
    '''
    if defaults is None:
        defaults = DEFAULT_OPTS

    overrides = _read_conf_file(path)
    opts = defaults.copy()
    if overrides:
        opts.update(overrides)
    return opts


# pylint: disable=W0212
def new_method_proxy(func):
    ''' Proxy function call to lazy get attrs '''
    def inner(self, *args):  # pylint: disable=C0111
        if self._wrapped is EMPTY:
            self._setup()
        return func(self._wrapped, *args)
    return inner
# pylint: enable=W0212


class LazyObject(object):
    '''
    Wrapper for another class to delay instantiation.
    '''
    _wrapped = None

    def __init__(self):
        self._wrapped = EMPTY

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is EMPTY:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError('can\'t delete _wrapped.')
        if self._wrapped is EMPTY:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        '''
        Must be implemented by subclasses to initialize wrapped object.
        '''
        raise NotImplementedError

    __dir__ = new_method_proxy(dir)


class LazySettings(LazyObject):
    '''
    Delay loading of settings.
    '''
    def _setup(self):
        settings_file = os.environ.get('YALP_CONFIG_FILE', None)
        self._wrapped = Settings(settings_file)
        self._configure_logging()

    def _configure_logging(self):
        ''' Configure logger from settings '''
        defauls = DEFAULT_LOGGING.copy()
        defauls['formatters']['simple']['format'] = self.log_format
        defauls['loggers']['yalp.inputs']['level'] = self.log_level
        defauls['loggers']['yalp.parsers']['level'] = self.log_level
        defauls['loggers']['yalp.outputs']['level'] = self.log_level
        dictConfig(defauls)
        if self.logging:
            dictConfig(self.logging)

    def update(self, update_dict):
        ''' Update settings from dict '''
        for key, val in update_dict.items():
            self.__setattr__(key, val)


class Settings(object):
    '''
    Load settings from yaml into object.
    '''
    def __init__(self, settings_file, defaults=None):
        opts = load_config(settings_file, defaults=defaults)
        for opt, value in opts.items():
            setattr(self, opt, value)


settings = LazySettings()

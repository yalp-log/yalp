# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.config
===========
'''
import os
import yaml

from .utils import LazyObject

import logging
logger = logging.getLogger(__name__)


DEFAULT_OPTS = {
    'broker_url': 'amqp://guest:guest@localhost:5672//',
    'parser_queue': 'parsers',
    'output_queue': 'outputs',
    'parser_worker_name': 'parser-workers',
    'output_worker_name': 'output-workers',
    'parser_workers': 5,
    'output_workers': 1,
    'celery_advanced': {},
    'inputs': [],
    'parsers': [],
    'outputs': [],
    'home': None,
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
            logger.error(
                'Error parsing configuration file: %s - %s', path, err)
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


class LazySettings(LazyObject):
    '''
    Delay loading of settings.
    '''
    def _setup(self):
        settings_file = os.environ.get('YALP_CONFIG_FILE', None)
        self._wrapped = Settings(settings_file)


class Settings(object):
    '''
    Load settings from yaml into object.
    '''
    def __init__(self, settings_file, defaults=None):
        opts = load_config(settings_file, defaults=defaults)
        for opt, value in opts.items():
            setattr(self, opt, value)


class UserSettingsHolder(object):
    '''
    Holder for user configured settings.
    '''
    def __init__(self, defaults=None):
        self.__dict__['_deleted'] = set()
        if not defaults:
            defaults = DEFAULT_OPTS
        self.default_settings = defaults

    def __getattr__(self, name):
        if name in self._deleted:
            raise AttributeError
        return getattr(self.default_settings, name)

    def __setattr__(self, name, value):
        self._deleted.discard(name)
        super(UserSettingsHolder, self).__setattr__(name, value)

    def __delattr__(self, name):
        self._deleted.add(name)
        if hasattr(self, name):
            super(UserSettingsHolder, self).__delattr__(name)

    def __dir__(self):
        return list(self.__dict__) + dir(self.default_settings)


settings = LazySettings()

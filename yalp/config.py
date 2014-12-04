# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.config
===========
'''
import os
import yaml

from .utils import LazyObject
from .exceptions import ImproperlyConfigured

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
    'parsers': [
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        }
    ],
    'outputs': [
        {
            'module': 'yalp.outputs.plain',
            'class': 'PlainOutputer',
        },
    ],
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
        for opt, value in opts.iteritems():
            setattr(self, opt, value)


settings = LazySettings()

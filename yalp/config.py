# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.config
===========
'''
import yaml

import logging

logger = logging.getLogger(__name__)


DEFAULT_OPTS = {
    'broker_url': 'amqp://guest:guest@localhost:5672//',
    'parser_queue': 'parsers',
    'output_queue': 'outputs',
    'parser_worker_name': 'parser-workers',
    'output_worker_name': 'output-workers',
}


DEFAULT_PARSER_OPTS = {
    'parsers': [
        {
            'module': 'yalp.parsers.plain',
            'class': 'PlainParser',
        }
    ],
}


DEFAULT_OUTPUT_OPTS = {
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


def load_parser_config(path, defaults=None):
    '''
    Read in config file.
    '''
    if defaults is None:
        defaults = DEFAULT_PARSER_OPTS

    overrides = _read_conf_file(path)
    opts = defaults.copy()
    if overrides:
        opts.update(overrides)
    return opts['parsers']


def load_output_config(path, defaults=None):
    '''
    Read in config file.
    '''
    if defaults is None:
        defaults = DEFAULT_OUTPUT_OPTS

    overrides = _read_conf_file(path)
    opts = defaults.copy()
    if overrides:
        opts.update(overrides)
    return opts['outputs']

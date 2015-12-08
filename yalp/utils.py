# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.utils
==========
'''
from .pipeline import BasePipline
from .exceptions import ImproperlyConfigured
from .config import settings


YALP_PLUGIN_MAPPINGS = {
    'input': {
        'classname': 'Inputer',
        'packages_list': 'input_packages',
    },
    'parser': {
        'classname': 'Parser',
        'packages_list': 'parser_packages',
    },
    'output': {
        'classname': 'Outputer',
        'packages_list': 'output_packages',
    },
}


def get_yalp_class(plugin, config, plugin_type, instance_type=BasePipline):
    '''
    Get a yalp input/parser/output class.
    '''
    class_name = YALP_PLUGIN_MAPPINGS[plugin_type]['classname']
    package_list = getattr(
        settings, YALP_PLUGIN_MAPPINGS[plugin_type]['packages_list'], [])

    for package in package_list:
        try:
            module_name = '.'.join([package, plugin])
            module = __import__(module_name, fromlist=[class_name])
            class_ = getattr(module, class_name)
            if 'type' in config:
                config['type_'] = config['type']
            instance = class_(**config)
            if not isinstance(instance, instance_type):
                raise ImportError
            return instance
        except (ImportError, NameError):
            pass
    raise ImproperlyConfigured('Invalid parser module/class.')


def get_hostname():
    '''
    Get system's hostname for worker process name.
    '''
    import socket
    hostname = socket.gethostname()
    del socket
    return hostname


def nested_get(data, lookup):
    '''
    Preform a nested dict and list lookup.
    '''
    for key in lookup.split(':'):
        if isinstance(data, list):
            try:
                idx = int(key)
                data = data[idx]
            except (ValueError, IndexError):
                raise KeyError
        else:
            try:
                data = data[key]
            except (KeyError, TypeError):
                raise KeyError
    return data


def nested_put(data, lookup, value):
    '''
    Update a field in a nested dict.
    '''
    try:
        initial_keys, last_key = lookup.rsplit(':', 1)
        data = nested_get(data, initial_keys)
    except ValueError:
        last_key = lookup
    data[last_key] = value

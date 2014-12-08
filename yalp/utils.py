# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.utils
==========
'''
from celery import Celery
from .pipeline import BasePipline
from .exceptions import ImproperlyConfigured

EMPTY = object()


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


def get_yalp_class(config, instance_type=BasePipline):
    '''
    Get a yalp input/parser/output class.
    '''
    try:
        module_name = config['module']
        print 'module: ' + module_name
        class_name = config['class']
        print 'class: ' + class_name
        module = __import__(module_name, fromlist=[class_name])
        class_ = getattr(module, class_name)
        if 'type' in config:
            config['type_'] = config['type']
            print 'type: ' + config['type']
        instance = class_(**config)
        if not isinstance(instance, instance_type):
            raise ImportError
        return instance
    except KeyError:
        raise ImproperlyConfigured('Invalid config: {0}'.format(config))
    except ImportError:
        raise ImproperlyConfigured('Invalid parser module/class.')


def get_celery_app(config):
    '''
    Create the parsers celery app.
    '''
    app = Celery()
    app.conf.update(
        BROKER_URL=config.broker_url,
        CELERY_ROUTES={
            'yalp.pipeline.tasks.process_message': {
                'queue': config.parser_queue,
            },
            'yalp.pipeline.tasks.process_output': {
                'queue': config.output_queue,
            },
        },
        **config.celery_advanced
    )
    app.autodiscover_tasks(lambda: (
        'yalp.pipeline',
    ))
    return app


def get_hostname():
    '''
    Get system's hostname for worker process name.
    '''
    import socket
    hostname = socket.gethostname()
    del socket
    return hostname

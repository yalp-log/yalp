# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs
============
'''
from celery import shared_task
from ..exceptions import ImproperlyConfigured


def _get_outputer(config):
    '''
    Get the outputer class from the config
    '''
    try:
        outputer_module_name = config['module']
        outputer_class_name = config['class']
        outputer_module = __import__(outputer_module_name,
                                     fromlist=[outputer_class_name])
        outputer_class = getattr(outputer_module, outputer_class_name)
        return outputer_class()
    except KeyError:
        raise ImproperlyConfigured('Invalid config.')
    except ImportError:
        raise ImproperlyConfigured('Invalid outputer module/class.')


@shared_task
def process_output(config, event):
    '''
    Output events
    '''
    for output_config in config:
        outputer = _get_outputer(output_config)
        outputer.output(event)

# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.tasks
==================
'''
from celery import shared_task
from ..exceptions import ImproperlyConfigured


def _get_outputer(config, **kwargs):
    '''
    Get the outputer class from the config
    '''
    try:
        outputer_module_name = kwargs['module']
        outputer_class_name = kwargs['class']
        outputer_module = __import__(outputer_module_name,
                                     fromlist=[outputer_class_name])
        outputer_class = getattr(outputer_module, outputer_class_name)
        return outputer_class(config, **kwargs)
    except KeyError:
        raise ImproperlyConfigured('Invalid config.')
    except ImportError:
        raise ImproperlyConfigured('Invalid outputer module/class.')


@shared_task
def process_output(config, event):
    '''
    Output events
    '''
    for output_config in config.get('outputs', []):
        outputer = _get_outputer(config, **output_config)
        outputer.output(event)

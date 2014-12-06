# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs
===========
'''
from ..config import settings
from ..utils import get_yalp_class, get_celery_app
from ..pipeline import ThreadPipline


class BaseInputer(ThreadPipline):
    ''' Base Inputer '''

    def __init__(self, *args, **kwargs):
        super(BaseInputer, self).__init__(*args, **kwargs)
        self.app = get_celery_app(settings)

    def enqueue_event(self, event):
        from yalp.pipeline import tasks
        if settings.parsers:
            tasks.process_message.apply_async(
                args=[event],
                queue=settings.parser_queue,
            )
        else:
            tasks.process_output.apply_async(
                args=[event],
                queue=settings.output_queue,
            )


def start_inputs():
    '''
    Start inputers
    '''
    config = settings.inputs
    inputers = [get_yalp_class(conf) for conf in config]
    for inputer in inputers:
        inputer.start()

    for inputer in inputers:
        inputer.join()

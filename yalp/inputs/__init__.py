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
        from yalp.pipeline import tasks
        if settings.parsers:
            self.process_task = tasks.process_message
            self.queue_name = settings.parser_queue
        else:
            self.process_task = tasks.process_output
            self.queue_name = settings.output_queue

    def enqueue_event(self, event):
        '''
        Take an event and send it to the proper queue.

        Send the event to the parsers queue, unless there are no parsers
        in the config. Then send the event directly to the outputs.
        '''
        self.process_task.apply_async(
            args=[event],
            queue=self.queue_name,
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

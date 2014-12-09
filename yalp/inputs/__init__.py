# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs
===========
'''
from ..config import settings
from ..utils import get_hostname
from ..pipeline import ThreadPipline


class BaseInputer(ThreadPipline):
    ''' Base Inputer '''

    def __init__(self, *args, **kwargs):
        super(BaseInputer, self).__init__(*args, **kwargs)
        self.hostname = get_hostname()
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
        if self.type_:
            event['type'] = self.type_
        event['hostname'] = self.hostname
        self.process_task.apply_async(
            args=[event],
            queue=self.queue_name,
        )

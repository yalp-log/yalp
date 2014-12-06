# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.file
================
'''
import tailer
from . import BaseInputer


class FileInputer(BaseInputer):
    '''
    Get input from a file.
    '''
    def __init__(self, path, type_=None, **kwargs):
        super(FileInputer, self).__init__(type_, **kwargs)
        self.path = path

    def run(self):
        with open(self.path, 'r') as in_file:
            for line in tailer.follow(in_file):
                event = {'message': line.strip()}
                if self.type_:
                    event['type'] = self.type_
                self.enqueue_event(event)

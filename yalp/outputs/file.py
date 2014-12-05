# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.file
=================
'''
import json
from . import BaseOutputer


class FileOutputer(BaseOutputer):
    '''
    Write output to a file.
    '''
    def __init__(self, path=None, *args, **kwargs):
        super(FileOutputer, self).__init__(*args, **kwargs)
        self.path = path

    def output(self, event):
        with open(self.path, 'a') as outfile:
            outfile.write(json.dumps(event))
            outfile.write('\n')

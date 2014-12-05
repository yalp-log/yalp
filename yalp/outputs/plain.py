# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.plain
==================
'''
from __future__ import print_function
from . import BaseOutputer


class PlainOutputer(BaseOutputer):
    '''
    Print output
    '''
    def __init__(self, *args, **kwargs):
        super(PlainOutputer, self).__init__(*args, **kwargs)

    def output(self, event):
        print(event)

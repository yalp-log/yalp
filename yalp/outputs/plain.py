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
    def output(self, event):
        print(event)
        super(PlainOutputer, self).output(event)


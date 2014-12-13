# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.passthrough
========================
'''
from __future__ import print_function
from . import BaseParser


class Parser(BaseParser):
    '''
    Print input
    '''
    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)

    def parse(self, event):
        print(event)
        return event

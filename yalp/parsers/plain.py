# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.nginx
==================
'''
from __future__ import print_function
from . import BaseParser


class PlainParser(BaseParser):
    '''
    Parse nginx log
    '''
    def parse(self, message):
        print(message)
        return super(PlainParser, self).parse(message)

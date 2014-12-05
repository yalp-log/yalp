# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.file
================
'''
from __future__ import print_function
from . import BaseInputer


class FileInputer(BaseInputer):
    '''
    Get input from a file.
    '''
    def __init__(self, path, type_=None, **kwargs):
        super(FileInputer, self).__init__(type_, **kwargs)
        self.path = path

    def run(self):
        print(self.path)

# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.stdout
===================
'''
from __future__ import print_function

import sys
import json
from . import BaseOutputer


class StdOutOutputer(BaseOutputer):
    '''
    Print output
    '''
    def __init__(self, out=sys.stdout, *args, **kwargs):
        super(StdOutOutputer, self).__init__(*args, **kwargs)
        self.out = out

    def output(self, event):
        self.out.write(json.dumps(event))

    def shutdown(self):
        pass


Outputer = StdOutOutputer

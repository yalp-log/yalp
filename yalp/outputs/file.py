# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.outputs.file
=================

The file outputer writes events to a file. Each event is recorded as a
JSON string.

This outputer supports the following configuration items:

**path**
    The path of the file to write the events.

*type*
    A type filter. Only output events of this type.

Example configutation.

.. code-block:: yaml

    outputs:
      - file:
          path: /var/log/all_messages

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
        self.outfile = open(self.path, 'a')

    def output(self, event):
        self.outfile.write(json.dumps(event) + '\n')

    def shutdown(self):
        self.outfile.flush()
        self.outfile.close()


Outputer = FileOutputer

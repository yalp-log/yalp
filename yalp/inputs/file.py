# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.file
================
'''
import os
import hashlib
import time
import tailer
from . import BaseInputer


class FileInputer(BaseInputer, tailer.Tailer):
    '''
    Get input from a file.
    '''
    def __init__(self, path, type_=None, read_size=1024, *args, **kwargs):
        super(FileInputer, self).__init__(type_, *args, **kwargs)
        self.path = path
        self.read_size = read_size
        self.sincedb_dir = os.environ['HOME']
        self.sincedb = os.path.join(
            self.sincedb_dir,
            '.sincedb_{0}'.format(hashlib.md5(self.path).hexdigest())
        )

    def _setup(self):
        '''
        Setup file handle seeking to last known position.
        '''
        self.file = open(self.path, 'r')
        self.start_pos = self.file.tell()
        if os.path.exists(self.sincedb):
            with open(self.sincedb, 'r') as sincedb_file:
                for line in sincedb_file.readlines():
                    position = line.strip()
                    self.seek(int(position))

    def stoppable_follow(self, delay=1.0):
        '''
        A tail follow that can be stopped on demand.
        '''
        trailing = True

        while 1:
            if self.stopped:
                break
            where = self.file.tell()
            line = self.file.readline()
            if line:
                if trailing and line in self.line_terminators:
                    trailing = False
                    continue

                if line[-1] in self.line_terminators:
                    line = line[:-1]
                    if line[-1:] == '\r\n' and '\r\n' in self.line_terminators:
                        # found crlf
                        line = line[:-1]

                trailing = False
                yield line
            else:
                trailing = True
                self.seek(where)
                time.sleep(delay)

    def _cleanup(self):
        '''
        Cleanup file handle, record current position.
        '''
        with open(self.sincedb, 'w') as sincedb_file:
            sincedb_file.write(str(self.file.tell()))
        self.file.close()

    def run(self):
        self._setup()
        for line in self.stoppable_follow():
            event = {'message': line}
            if self.type_:
                event['type'] = self.type_
            self.enqueue_event(event)
        self._cleanup()

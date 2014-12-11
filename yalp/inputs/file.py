# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs.file
================
'''
import os
import hashlib
import time
from ..config import settings
from . import BaseInputer


class Inputer(BaseInputer):
    '''
    Get input from a file.
    '''
    line_terminators = ('\r\n', '\n', '\r')

    def __init__(self, path, *args, **kwargs):
        super(Inputer, self).__init__(*args, **kwargs)
        self.path = path
        self.sincedb_dir = settings.home or os.environ['HOME']
        self.sincedb = os.path.join(
            self.sincedb_dir,
            '.sincedb_{0}'.format(hashlib.md5(self.path).hexdigest())
        )

    def _setup(self):
        '''
        Setup file handle seeking to last known position.
        '''
        self.file = open(self.path, 'r')
        self.cur_inode = os.fstat(self.file.fileno()).st_ino
        if os.path.exists(self.sincedb):
            with open(self.sincedb, 'r') as sincedb_file:
                for line in sincedb_file.readlines():
                    inode, position = line.strip().split()
                    if int(inode) == self.cur_inode:
                        self.file.seek(int(position))

    def _cleanup(self):
        '''
        Cleanup file handle, record current position.
        '''
        self._write_sincedb()
        self.file.close()

    def _write_sincedb(self):
        ''' Write current state to sincedb '''
        with open(self.sincedb, 'w') as sincedb_file:
            sincedb_file.write('{0} {1}'.format(self.cur_inode,
                                                self.file.tell()))

    def _follow(self, delay=1.0):
        '''
        Iterator generator that returns lines as data is added to the
        file. Iteration will stop when thread is triggered to stop.

        Based on:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
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
                if os.stat(self.path).st_ino != self.cur_inode:
                    new_file = open(self.path, 'r')
                    self.file.close()
                    self.file = new_file
                    self.cur_inode = os.fstat(self.file.fileno()).st_ino
                    self._write_sincedb()
                else:
                    self.file.seek(where)
                time.sleep(delay)

    def run(self):
        self._setup()
        for line in self._follow():
            event = {'message': line}
            self.enqueue_event(event)
        self._cleanup()

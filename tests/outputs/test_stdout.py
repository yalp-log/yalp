# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.outputs.test_stdout
========================
'''
import unittest
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from yalp.outputs import stdout


class TestStdoutOutput(unittest.TestCase):
    '''
    Test the stdout.Outputer
    '''
    def test_output_event(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'time_stamp': '2015-01-01T00:00:00',
        }
        out = StringIO()
        outputer = stdout.Outputer(out=out)
        outputer.run(event)
        outputer.shutdown()
        output = out.getvalue().strip()
        self.assertEqual(output, json.dumps(event))

    def test_output_event_skip_on_type(self):
        event = {
            'host': 'localhost',
            'message': 'test message',
            'type': 'no out',
            'time_stamp': '2015-01-01T00:00:00',
        }
        out = StringIO()
        outputer = stdout.Outputer(out=out)
        outputer.run(event)
        outputer.shutdown()
        output = out.getvalue().strip()
        self.assertEqual(output, '')

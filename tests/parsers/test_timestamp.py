# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_timestamp
============================
'''
import unittest
from yalp.parsers import timestamp


class TestTimestampParser(unittest.TestCase):
    '''
    Test the timestamp.Parser
    '''

    def test_parse_event(self):
        event = {
            'host': 'localhost',
            'message': u'127.0.0.1 - - [13/Mar/2014:13:46:00 -0400] "GET / HTTP/1.1" 200 6301 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0" "6.57"',
            'date_field': u'13/Mar/2014:13:46:00 -0400',
            'time_stamp': '2015-01-01T00:00:00',
        }
        parser = timestamp.Parser(field='date_field')
        parsed_event = parser.run(event)
        self.assertEqual('2014-03-13T13:46:00', parsed_event['time_stamp'])

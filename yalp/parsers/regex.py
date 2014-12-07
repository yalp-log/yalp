# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.regex
==================
'''
import re
from . import BaseParser


class RegexParser(BaseParser):
    '''
    Process input with regex.
    '''
    def __init__(self, regex=None, *args, **kwargs):
        super(RegexParser, self).__init__(*args, **kwargs)
        self.regex = regex

    def parse(self, event):
        message = event.pop('message')
        match = re.match(self.regex, message)
        if match:
            event.update(match.groupdict())
            return event
        else:
            return None

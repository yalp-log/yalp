# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.regex
==================

The regex parser applies a regex to the message of an event. Any named
components of the regex become new keys in the event dict with the
matched strings becoming the values.

.. note::
    The original message is removed from the event.

This parser supports the following configuration items:

**regex**
    The regex to apply.

*type*
    A type filter. Only apply the regex to events of this type.


Example configuration.

.. code-block:: yaml

    parsers:
      - regex:
          regex: '(?P<month>\\w+)\\s+(?P<day>\\d+)'

'''
import re
from . import ExtractFieldParser


class RegexParser(ExtractFieldParser):
    '''
    Process input with regex.
    '''
    def __init__(self, regex=None, *args, **kwargs):
        super(RegexParser, self).__init__(*args, **kwargs)
        self.regex = regex

    def parse(self, event):
        message = self.data
        match = re.match(self.regex, message)
        if match:
            event.update(match.groupdict())
        return event


Parser = RegexParser

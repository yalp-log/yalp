# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.grok
=================

Use `grok`_ to parse the event. Any matched fields from the grok pattern
will be added to the event.

This parser supports the following connfiguration items:

**pattern**
    A grok pattern to match. See `available patterns`_ for details.

*field*
    The field from the event to parse. Defaults to ``message``.

*type*
    A type filter. Events not of this type will be skipped.


Example configuration.

.. code-block:: yaml

    parsers:
      - grok:
        pattern: '%{IP:ip_addr} %{WORD:request_type} %{URIPATHPARAM:path}'

With an input event like the following:

.. code-block:: python

    {
        'message': '192.168.0.1 GET /index.html',
        'time_stamp': '2015-01-01T01:00:00',
        'hostname': 'server_hostname',
    }

After the parser runs, the event will become:

.. code-block:: python

    {
        'message': '192.168.0.1 GET /index.html',
        'time_stamp': '2015-01-01T01:00:00',
        'hostname': 'server_hostname',
        'ip_addr': '192.168.0.1',
        'request_type': 'GET',
        'path': '/index.html',
    }

.. _available patterns: https://github.com/garyelephant/pygrok/tree/master/pygrok/patterns
.. _grok: https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html#plugins-filters-grok
'''
import yalp_grok as grok
from . import ExtractFieldParser


class GrokParser(ExtractFieldParser):
    '''
    Process input with grok pattern match.
    '''
    def __init__(self, field='message', pattern=None, *args, **kwargs):
        super(GrokParser, self).__init__(field, *args, **kwargs)
        self.pattern = pattern
        self.compiled_pattern = grok.compile_pattern(self.pattern)

    def parse(self, event):
        matches = grok.grok_search(self.data, self.compiled_pattern)
        if matches:
            event.update(matches)
        return event


Parser = GrokParser

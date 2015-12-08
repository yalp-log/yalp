# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.url
================

Extract components of a url.

The parser supports the following configuration items:

*field*
    The field containing the url string to parse. If the field is not
    found in the event, the event will be skipped. Defaults to
    ``request``.

*out_field*
    The field to set the url components to. Defaults to ``url``.

*type*
    A type filter. Events not of this type will be skipped.


Example configuration.

.. code-block:: yaml

    parsers:
      - url:
          field: 'request'

With an input event like the following:

.. code-block:: python

    {
        'hostname': 'server_hostname',
        'time_stamp': '2015-01-01T01:00:00',
        'request': '/index.html?param1=val1&param2=val2',
    }

After the parser runs, the event will become:

.. code-block:: python

    {
        'hostname': 'server_hostname',
        'time_stamp': '2015-01-01T01:00:00',
        'request': '/index.html?param1=val1&param2=val2',
        'url': {
            'fragment': '',
            'hostname': None,
            'netloc': '',
            'params': '',
            'password': None,
            'path': '/index.html',
            'port': None,
            'query': {
                'param1': ['val1'],
                'param2': ['val2'],
            },
            'scheme': '',
            'username': None
        },
    }

'''
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    # pylint: disable=no-name-in-module,import-error
    from urllib.parse import urlparse, parse_qs
    # pylint: enable=no-name-in-module,import-error

from yalp.parsers import ExtractFieldParser


class UrlParser(ExtractFieldParser):
    '''
    Split urls into components.
    '''
    def __init__(self,
                 field='request',
                 out_field='url',
                 *args,
                 **kwargs):
        super(UrlParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field

    def parse(self, event):
        url_str = self.data
        url_parts = urlparse(url_str)
        query_params = parse_qs(url_parts.query)
        event[self.out_field] = {
            'scheme': url_parts.scheme,
            'netloc': url_parts.netloc,
            'path': url_parts.path,
            'params': url_parts.params,
            'query': query_params,
            'fragment': url_parts.fragment,
            'username': url_parts.username,
            'password': url_parts.password,
            'hostname': url_parts.hostname,
            'port': url_parts.port,
        }
        return event


Parser = UrlParser

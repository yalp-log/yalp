# vim: set et ts=4 sw=4 fileencoding=utf-8:
# pylint: disable=line-too-long
'''
yalp.parsers.user_agent
=======================

Extract browser, OS, device and other information from a user agent
string.

The parser supports the following configuration items:

*field*
    The field containing the user agent string to parse. If the field is
    not found in the event, the event will be skipped. Defaults to
    ``agent``.

*out_field*
    Set this to a field to store the user agent information under. If not
    set, the new field are added at the top level of the event.

*type*
    A type filter. Events not of this type will be skipped.


Example configuration.

.. code-block:: yaml

    parsers:
      - user_agent:
          field: 'agent'
          out_field: 'user_agent'

With an input event like the following:


.. code-block:: python

    {
        'hostname': 'server_hostname',
        'time_stamp': '2015-01-01T01:00:00',
        'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
    }

After the parser runs, the event will become:

.. code-block:: python

    {
        'hostname': 'server_hostname',
        'time_stamp': '2015-01-01T01:00:00',
        'message': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        'agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"',
        'user_agent': {
            'os': {
                'family': 'Linux',
                'version': ''
            },
            'browser': {
                'family': 'Firefox',
                'version': '38'
            },
            'device': {
                'brand': None,
                'family': 'Other',
                'model': None,
            },
            'is_bot': False,
            'is_mobile': False,
            'is_pc': True,
            'is_tablet': False,
            'is_touch_capable': False,
        },
    }
'''
# pylint: enable=line-too-long
import user_agents
from . import ExtractFieldParser


class UserAgentParser(ExtractFieldParser):
    '''
    Extract OS and Broswer info from user agent string
    '''
    def __init__(self,
                 field='agent',
                 out_field=None,
                 *args,
                 **kwargs):
        super(UserAgentParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field

    def parse(self, event):
        ua_str = self.data
        ua = user_agents.parse(ua_str)
        ua_data = {
            'browser': {
                'family': ua.browser.family,
                'version': ua.browser.version_string,
            },
            'os': {
                'family': ua.os.family,
                'version': ua.os.version_string,
            },
            'device': {
                'family': ua.device.family,
                'brand': ua.device.brand,
                'model': ua.device.model,
            },
            'is_mobile': ua.is_mobile,
            'is_tablet': ua.is_tablet,
            'is_touch_capable': ua.is_touch_capable,
            'is_pc': ua.is_pc,
            'is_bot': ua.is_bot,
        }
        if self.out_field:
            event[self.out_field] = ua_data
        else:
            event.update(ua_data)
        return event


Parser = UserAgentParser

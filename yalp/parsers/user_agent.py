# vim: set et ts=4 sw=4 fileencoding=utf-8:
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


Example configuration/

.. code-block:: yaml

    parsers:
      - user_agent:
          field: 'agent'
          out_field: 'user_agent'
'''
import user_agents
from . import BaseParser


class Parser(BaseParser):
    '''
    Extract OS and Broswer info from user agent string
    '''
    def __init__(self,
                 field='agent',
                 out_field=None,
                 *args,
                 **kwargs):
        super(Parser, self).__init__(*args, **kwargs)
        self.field = field
        self.out_field = out_field

    def parse(self, event):
        if self.field in event:
            ua_str = event[self.field]
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

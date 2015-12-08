# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.json
=================

Load json data.

The parser supports the following configuration items:

*field*
    The field containing the json string to load. Defaults to ``message``.

*out_field*
    Set this to a field to store the loaded dict. If not set, the new
    fields are added at the top level of the event.

*type*
    A type filter. Events not of this type will be skipped.
'''
from __future__ import absolute_import
import json
from . import ExtractFieldParser


class JsonParser(ExtractFieldParser):
    '''
    Load json data.
    '''
    def __init__(self,
                 field='message',
                 out_field=None,
                 *args,
                 **kwargs):
        super(JsonParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field

    def parse(self, event):
        json_str = self.data
        try:
            data = json.loads(json_str)
            if self.out_field:
                event[self.out_field] = data
            else:
                event.update(data)
        except ValueError:
            self.logger.error('Failed to load json')
        return event


Parser = JsonParser

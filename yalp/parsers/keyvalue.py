# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.keyvalue
=====================

Extract key, value paired data.

The parser supports the following configuration items:

**field**
    The field containing the key value pairs to parse.

*out_field*
    Set this to a field to store the parsed pairs under. If not set, the
    new fields are added at the top level of the event.

*sep*
    The seperator between key and value in a pair. Defaults to ``:``

*pair_sep*
    The seperator between pairs of key/values. Defaults to a single space.

*type*
    A type filter. Events not of this type will be skipped.
'''
from . import ExtractFieldParser


class KeyValueParser(ExtractFieldParser):
    '''
    Extract key value data.
    '''
    def __init__(self,
                 field,
                 out_field=None,
                 sep=':',
                 pair_sep=' ',
                 *args,
                 **kwargs):
        super(KeyValueParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field
        self.sep = sep
        self.pair_sep = pair_sep

    def parse(self, event):
        pairs = self.data.split(self.pair_sep)  # pylint: disable=no-member
        keyvalues = {}
        for pair in pairs:
            key, value = pair.split(self.sep, 1)
            keyvalues[key] = value
        if self.out_field:
            event[self.out_field] = keyvalues
        else:
            event.update(keyvalues)
        return event


Parser = KeyValueParser

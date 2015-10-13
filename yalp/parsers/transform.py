# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.transform
======================

Used to convert a field in the event to a different built-in type.

The parser supports the following configuration items:

..note::
    If the field fails to be transformed, The parser will log an error
    and leave the field as it was originally.

**field**
    The field to convert. If the field is not found in the event, the
    event will be skipped.

**to**
    Convert the field into this type. Supported types are::

        int
        float
        str

*type*
    A type filter. Events not of this type will be skipped.


Example configuration.

.. code-block:: yaml

    parsers:
      - transform:
          field: response_time
          to: int
'''
from . import BaseParser


def _to_int(field):
    ''' Transform to int '''
    return int(field)


def _to_float(field):
    ''' Transform to float '''
    return float(field)


def _to_str(field):
    ''' Transform to str '''
    return str(field)


TRANSFORM_MAP = {
    'int': _to_int,
    'float': _to_float,
    'str': _to_str,
}


class TransformParser(BaseParser):
    '''
    Transform fields into new field types.
    '''
    def __init__(self, field, to, *args, **kwargs):
        super(TransformParser, self).__init__(*args, **kwargs)
        self.field = field
        self.to = to
        self.to_func = TRANSFORM_MAP[self.to]

    def parse(self, event):
        if self.field in event:
            try:
                event[self.field] = self.to_func(event[self.field])
            except ValueError:
                self.logger.error('Failed to transform field %s to %s',
                                  self.field,
                                  self.to)
        return event


Parser = TransformParser

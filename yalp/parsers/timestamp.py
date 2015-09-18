# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.timestamp
======================

Used to set the event time_stamp from another field in the event.

The parser supports the following configuration items:

**field**
    The field to parse for a datetime. If the field is not found in the
    event, the event will be skipped.

*out_field*
    The field to write the parsed time stamp to. Defaults to
    ``time_stamp``.

*timestamp_fmt*
    The `date format`_ string to format the time stamp. Defaults to
    ``%Y-%m-%dT$H:%M:%S``.

*type*
    A type filter. Events not of this type will be skipped.


Examaple configuration.

.. code-block:: yaml

    parsers:
      - timestamp:
          field: date_field

.. _date format: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
from dateutil.parser import parse as dt_parse

from . import BaseParser

DEFAULT_DATE_FMT = '%Y-%m-%dT%H:%M:%S'


class TimeStampParser(BaseParser):
    '''
    Search for datetime string and set time_stamp.
    '''
    def __init__(self,
                 field,
                 out_field='time_stamp',
                 timestamp_fmt=DEFAULT_DATE_FMT,
                 *args,
                 **kwargs):
        super(TimeStampParser, self).__init__(*args, **kwargs)
        self.field = field
        self.out_field = out_field
        self.timestamp_fmt = timestamp_fmt

    def parse(self, event):
        if self.field in event:
            event[self.out_field] = dt_parse(  # pylint: disable=no-member
                event[self.field],
                fuzzy=True
            ).strftime(self.timestamp_fmt)
        return event


Parser = TimeStampParser

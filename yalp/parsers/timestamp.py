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

*to_utc*
    Convert the timestamp to UTC after parsing. Defaults to ``True``.

*type*
    A type filter. Events not of this type will be skipped.


Examaple configuration.

.. code-block:: yaml

    parsers:
      - timestamp:
          field: date_field

.. _date format: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
from dateutil import tz
from dateutil.parser import parse as dt_parse

from . import ExtractFieldParser

DEFAULT_DATE_FMT = '%Y-%m-%dT%H:%M:%S'
UTC = tz.tzutc()


class TimeStampParser(ExtractFieldParser):
    '''
    Search for datetime string and set time_stamp.
    '''
    def __init__(self,
                 field='timestamp',
                 out_field='time_stamp',
                 timestamp_fmt=DEFAULT_DATE_FMT,
                 to_utc=True,
                 *args,
                 **kwargs):
        super(TimeStampParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field
        self.timestamp_fmt = timestamp_fmt
        self.to_utc = to_utc

    def parse(self, event):
        parsed_dt = dt_parse(self.data, fuzzy=True)
        # pylint: disable=no-member
        if self.to_utc:
            try:
                parsed_dt = parsed_dt.astimezone(UTC)
            except ValueError:
                self.logger.info('Failed to convert to UTC')
        event[self.out_field] = parsed_dt.strftime(self.timestamp_fmt)
        # pylint: enable=no-member
        return event


Parser = TimeStampParser

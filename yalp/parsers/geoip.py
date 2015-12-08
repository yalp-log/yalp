# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.geoip
==================

Extract Geo location data from an IP address.

The parser supports the following configuration items:

.. warning::
    This parser requires the pygeoip_ package. The pygeoip package
    uses MaxMind's GeoIP dat files to get geo info from IP addresses.
    See http://dev.maxmind.com/geoip/legacy/geolite/ for more info.

.. note::
    The geohash_ package is nessecary for converting latitude/longitude
    into geohashes. If not installed, the parser will store the raw
    latitude and longitude.

**geoip_dat**
    Path to the MaxMind GeoIP City dat file.

*field*
    The field containing the IP address to parse. If the field is not
    found in the event, the event will be skipped. Defaults to
    ``clientip``.

*out_field*
    The field to set the Geo data to. Defaults to ``geoip``.

*use_hash*
    Store location as a geohash. Default is ``True``. If set to ``False``
    location will be stored as ['lat', 'lon'] pair. Ignored if `geohash`_
    is not installed.

*type*
    A type filter. Events not of this type will be skipped.


Example configuration.

.. code-block:: yaml

    parsers:
      - geoip:
          field: 'clientip'
          geoip_dat: '/usr/share/GeoLiteCity.dat'


.. _pygeoip: https://pypi.python.org/pypi/pygeoip/
.. _geohash: https://pypi.python.org/pypi/python-geohash
'''
try:
    import geohash
    HAS_GEOHASH = True
except ImportError:
    HAS_GEOHASH = False

from pygeoip import GeoIP, GeoIPError
from . import ExtractFieldParser


def _loc_geohash(geo_info):
    ''' Create location with geohash '''
    return geohash.encode(
        geo_info.pop('latitude'),
        geo_info.pop('longitude'),
    )


def _loc_point(geo_info):
    ''' Create location as point [lon, lat] '''
    return [
        geo_info.pop('longitude'),
        geo_info.pop('latitude'),
    ]


class GeoIPParser(ExtractFieldParser):
    '''
    Get geo info from IP address.
    '''
    def __init__(self,
                 field='clientip',
                 out_field='geoip',
                 geoip_dat='',
                 use_hash=True,
                 *args,
                 **kwargs):
        super(GeoIPParser, self).__init__(field, *args, **kwargs)
        self.out_field = out_field
        self.get_loc = _loc_geohash if HAS_GEOHASH and use_hash else _loc_point
        try:
            self.geoip = GeoIP(geoip_dat)
        except (IOError, GeoIPError) as exc:
            self.logger.error('Invalid GeoIP Database file: %s', geoip_dat)
            raise exc

    def parse(self, event):
        ip_addr = self.data
        try:
            geo_info = self.geoip.record_by_addr(ip_addr)
            if 'latitude' in geo_info and 'longitude' in geo_info:
                geo_info['location'] = self.get_loc(geo_info)
            event[self.out_field] = geo_info
        except (IndexError, TypeError):
            self.logger.warn('Failed to get Geo info from ip: %s', ip_addr)
        return event


Parser = GeoIPParser

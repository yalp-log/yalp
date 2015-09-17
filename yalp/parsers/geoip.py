# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.geoip
==================
'''
try:
    import geohash
    HAS_GEOHASH = True
except ImportError:
    HAS_GEOHASH = False

from pygeoip import GeoIP, GeoIPError
from . import BaseParser


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


class Parser(BaseParser):
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
        super(Parser, self).__init__(*args, **kwargs)
        self.field = field
        self.out_field = out_field
        self.get_loc = _loc_geohash if HAS_GEOHASH and use_hash else _loc_point
        try:
            self.geoip = GeoIP(geoip_dat)
        except (IOError, GeoIPError) as exc:
            self.logger.error('Invalid GeoIP Database file: %s', geoip_dat)
            raise exc

    def parse(self, event):
        if self.field in event:
            ip_addr = event[self.field]
            try:
                geo_info = self.geoip.record_by_addr(ip_addr)
                if 'latitude' in geo_info and 'longitude' in geo_info:
                    geo_info['location'] = self.get_loc(geo_info)
                event[self.out_field] = geo_info
            except (IndexError, TypeError):
                self.logger.warn('Failed to get Geo info from ip: %s', ip_addr)
        return event

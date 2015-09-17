# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.geoip
==================
'''
import geohash
from pygeoip import GeoIP, GeoIPError
from . import BaseParser


class Parser(BaseParser):
    '''
    Get geo info from IP address.
    '''
    def __init__(self,
                 field='agent',
                 out_field='geoip',
                 geoip_dat=None,
                 *args,
                 **kwargs):
        super(Parser, self).__init__(*args, **kwargs)
        self.field = field
        self.out_field = out_field
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
                if 'lattitude' in geo_info and 'longitude' in geo_info:
                    location = geohash.encode(geo_info.pop('lattitude'),
                                              geo_info.pop('longitude'))
                    geo_info['location'] = location
                event[self.out_field] = geo_info
            except (IndexError, TypeError):
                self.logger.warn('Failed to get Geo info from ip: %s', ip_addr)
        return event

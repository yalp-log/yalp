# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
tests.parsers.test_geoip
========================
'''
import os
import unittest

import geohash
from pygeoip import GeoIP

from yalp.parsers import geoip



class TestGeoipParserMissingDat(unittest.TestCase):
    '''
    Test the geoip.Parser
    '''
    def test_missing_dat(self):
        with self.assertRaises(IOError):
            geoip.Parser()


class TestGeoipParser(unittest.TestCase):
    '''
    Test the geoip.Parser
    '''
    def setUp(self):
        self.test_dat_file = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'GeoLiteCity.dat',
        ))
        if not os.path.isfile(self.test_dat_file):
            from nose.plugins.skip import SkipTest
            raise SkipTest('No GeoLiteCity dat file')

    def expected_hash(self, ip_address):
        g = GeoIP(self.test_dat_file)
        geo_info = g.record_by_addr(ip_address)
        return geohash.encode(
            geo_info.pop('latitude'),
            geo_info.pop('longitude'),
        )

    def expected_loc_point(self, ip_address):
        g = GeoIP(self.test_dat_file)
        geo_info = g.record_by_addr(ip_address)
        return [
            geo_info.pop('longitude'),
            geo_info.pop('latitude'),
        ]

    def test_geoip(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'clientip': '8.8.4.4',
        }
        parser = geoip.Parser(geoip_dat=self.test_dat_file)
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'clientip': '8.8.4.4',
            'geoip': {
                'area_code': 0,
                'city': None,
                'continent': 'NA',
                'country_code': 'US',
                'country_code3': 'USA',
                'country_name': 'United States',
                'dma_code': 0,
                'location': self.expected_hash('8.8.4.4'),
                'metro_code': None,
                'postal_code': None,
                'region_code': None,
                'time_zone': None
            },
        }
        self.assertDictEqual(expected, parsed_event)

    def test_geoip_no_geohash(self):
        event = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'clientip': '8.8.4.4',
        }
        parser = geoip.Parser(geoip_dat=self.test_dat_file, use_hash=False)
        parsed_event = parser.run(event)
        expected = {
            'hostname': 'server_hostname',
            'time_stamp': '2015-01-01T01:00:00',
            'clientip': '8.8.4.4',
            'geoip': {
                'area_code': 0,
                'city': None,
                'continent': 'NA',
                'country_code': 'US',
                'country_code3': 'USA',
                'country_name': 'United States',
                'dma_code': 0,
                'location': self.expected_loc_point('8.8.4.4'),
                'metro_code': None,
                'postal_code': None,
                'region_code': None,
                'time_zone': None
            },
        }
        self.assertDictEqual(expected, parsed_event)

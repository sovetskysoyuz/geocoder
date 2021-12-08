#!/usr/bin/python
# coding: utf8
from __future__ import absolute_import

import logging
import json
import ratelim

from geocoderliqr.osm import OsmResult, OsmQuery
from geocoderliqr.keys import locationiq_key


class LocationIQResult(OsmResult):
    pass


class LocationIQQuery(OsmQuery):
    provider = 'locationiq'
    method = 'geocode'

    _URL = 'https://locationiq.org/v1/search.php'
    _RESULT_CLASS = LocationIQResult
    _KEY = locationiq_key
    _KEY_MANDATORY = True

    def _build_params(self, location, provider_key, **kwargs):
        if 'limit' in kwargs:
            kwargs['maxRows'] = kwargs['limit']
        self.rate_limit = kwargs.get('rate_limit', True)
        return {
            'key': provider_key,
            'q': location,
            'format': 'json',
            'addressdetails': 1,
            'limit': kwargs.get('maxRows', 1),
        }
        
    def rate_limited_get(self, *args, **kwargs):
        if not self.rate_limit:
            return super(LocationIQQuery, self).rate_limited_get(*args, **kwargs)
        elif False:
            return self.rate_limited_get_for_work(*args, **kwargs)
        else:
            return self.rate_limited_get_for_dev(*args, **kwargs)

    @ratelim.greedy(4500, 60 * 60 * 24)
    @ratelim.greedy(1, 1)
    def rate_limited_get_for_dev(self, *args, **kwargs):
        return super(LocationIQQuery, self).rate_limited_get(*args, **kwargs)

    @ratelim.greedy(4500, 60 * 60 * 24)  # Google for Work daily limit
    @ratelim.greedy(1, 1)  # Google for Work limit per second
    def rate_limited_get_for_work(self, *args, **kwargs):
        return super(LocationIQQuery, self).rate_limited_get(*args, **kwargs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    g = LocationIQQuery('Ottawa, Ontario')
    g.debug()
    g = LocationIQQuery('Ottawa, Ontario', maxRows=5)
    print(json.dumps(g.geojson, indent=4))

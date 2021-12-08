#!/usr/bin/python
# coding: utf8

import geocoderliqr as geocoder


def test_unicode():
    g = geocoder.google('東京', key='')
    assert g


def test_repr_unicode():
    g = geocoder.osm('Tokyo, Japan')
    assert g

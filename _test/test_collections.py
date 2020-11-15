# coding: utf-8

"""
collections.OrderedDict is a new class not supported by PyYAML (issue 83 by Frazer McLean)

This is now so integrated in Python that it can be mapped to !!omap

"""

import pytest  # NOQA
from roundtrip import dedent, round_trip, round_trip_dump, round_trip_load  # NOQA


class TestOrderedDict:
    def test_ordereddict(self):
        from collections import OrderedDict

        import ruyaml  # NOQA

        assert ruyaml.dump(OrderedDict()) == '!!omap []\n'

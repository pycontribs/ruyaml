# coding: utf-8

"""
testing of anchors and the aliases referring to them
"""

import pytest
from textwrap import dedent

import ruamel.yaml
from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump

def load(s):
    return round_trip_load(dedent(s))

def compare(data, s):
    assert round_trip_dump(data) == dedent(s)


class TestAnchorsAliases:
    def test_anchor_id_renumber(self):
        from ruamel.yaml.serializer import Serializer
        assert Serializer.ANCHOR_TEMPLATE == 'id%03d'
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        """)
        compare(data, """
        a: &id001
          b: 1
          c: 2
        d: *id001
        """)

    def test_template_matcher(self):
        """test if id matches the anchor template"""
        from ruamel.yaml.serializer import templated_id
        assert templated_id(u'id001')
        assert templated_id(u'id999')
        assert templated_id(u'id1000')
        assert templated_id(u'id0001')
        assert templated_id(u'id0000')
        assert not templated_id(u'id02')
        assert not templated_id(u'id000')
        assert not templated_id(u'x000')

    #def test_re_matcher(self):
    #    import re
    #    assert re.compile(u'id(?!000)\\d{3,}').match('id001')
    #    assert not re.compile(u'id(?!000\\d*)\\d{3,}').match('id000')
    #    assert re.compile(u'id(?!000$)\\d{3,}').match('id0001')

    def test_anchor_assigned(self):
        from ruamel.yaml.comments import CommentedMap
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)
        d = data['d']
        assert isinstance(d, CommentedMap)
        assert d.yaml_anchor() is None  # got dropped as it matches pattern
        e = data['e']
        assert isinstance(e, CommentedMap)
        assert e.yaml_anchor() == 'etemplate'

    #@pytest.mark.xfail
    def test_anchor_id_retained(self):
        data = load("""
        a: &id002
          b: 1
          c: 2
        d: *id002
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)
        compare(data, """
        a: &id001
          b: 1
          c: 2
        d: *id001
        e: &etemplate
          b: 1
          c: 2
        f: *etemplate
        """)

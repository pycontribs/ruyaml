
from __future__ import print_function

"""
various test cases for YAML files
"""

import pytest

import ruamel.yaml
from ruamel.yaml.compat import ordereddict
from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump


class TestYAML:
    def test_backslash(self):
        round_trip("""
        handlers:
          static_files: applications/\\1/static/\\2
        """)

    def test_omap_out(self):
        # ordereddict mapped to !!omap
        x = ordereddict([('a', 1), ('b', 2)])
        res = ruamel.yaml.dump(x, default_flow_style=False)
        assert res == dedent("""
        !!omap
        - a: 1
        - b: 2
        """)

    def test_omap_roundtrip(self):
        round_trip("""
        !!omap
        - a: 1
        - b: 2
        - c: 3
        - d: 4
        """)

    def test_CommentedSet(self):
        from ruamel.yaml.constructor import CommentedSet
        s = CommentedSet(['a', 'b', 'c'])
        s.remove('b')
        s.add('d')
        assert s == CommentedSet(['a', 'c', 'd'])
        s.add('e')
        s.add('f')
        s.remove('e')
        assert s == CommentedSet(['a', 'c', 'd', 'f'])

    def test_set_out(self):
        # preferable would be the shorter format without the ': null'
        from ruamel.yaml.compat import ordereddict
        x = set(['a', 'b', 'c'])
        res = ruamel.yaml.dump(x, default_flow_style=False)
        assert res == dedent("""
        !!set
        a: null
        b: null
        c: null
        """)

    # @pytest.mark.xfail
    # ordering is not preserved in a set
    def test_set_compact(self):
        # this format is read and also should be written by default
        round_trip("""
        !!set
        ? a
        ? b
        ? c
        """)

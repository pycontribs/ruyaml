from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

import ruamel.yaml


def rt(s):
    return ruamel.yaml.dump(
        ruamel.yaml.load(s, Loader=ruamel.yaml.RoundTripLoader),
        Dumper=ruamel.yaml.RoundTripDumper,
    ).strip() + '\n'


@pytest.mark.xfail
def test_roundtrip_inline_list():
    s = 'a: [a, b, c]\n'
    output = rt(s)
    assert s == output


@pytest.mark.xfail
def test_roundtrip_four_space_indents():
    s = (
        'a:\n'
        '-   foo\n'
        '-   bar\n'
    )
    output = rt(s)
    assert s == output

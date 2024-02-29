import io
from typing import Any, Dict, List, Text  # NOQA

import pytest

import ruyaml  # NOQA
from ruyaml import YAML
from ruyaml.comments import CommentedSeq
from ruyaml.constructor import RoundTripConstructor
from ruyaml.representer import RoundTripRepresenter, ScalarNode
from ruyaml.scalarbool import ScalarBoolean
from ruyaml.util import load_yaml_guess_indent

from .roundtrip import dedent, round_trip


def round_trip_stabler(
    inp,
    outp=None,
):
    if outp is None:
        outp = inp
    doutp = dedent(outp)
    yaml = ruyaml.YAML()
    yaml.preserve_quotes = True
    yaml.preserve_bools = True
    data = yaml.load(doutp)
    buf = io.StringIO()
    yaml.dump(data, stream=buf)
    res = buf.getvalue()
    assert res == doutp


class TestStability:
    def test_lowercase_boolean(self):
        round_trip(
            """
        - true
        """
        )

    @pytest.mark.xfail(strict=True)
    def test_uppercase_boolean(self):
        round_trip(
            """
        - True
        """
        )

    # @pytest.mark.xfail(strict=True)  # Why not failing??
    def test_yes_boolean(self):
        round_trip(
            """
        - yes
        """
        )

    def test_lowercase_boolean2(self):
        round_trip_stabler(
            """
        - true
        """
        )

    def test_uppercase_boolean2(self):
        round_trip_stabler(
            """
        - True
        """
        )

    def test_yes_boolean2(self):
        round_trip_stabler(
            """
        - yes
        """
        )

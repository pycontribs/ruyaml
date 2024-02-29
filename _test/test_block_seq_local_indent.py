
import pytest
import io
import ruyaml  # NOQA
from .roundtrip import round_trip, dedent

from ruyaml import YAML
from ruyaml.util import load_yaml_guess_indent
from ruyaml.scalarbool import ScalarBoolean
from ruyaml.comments import CommentedSeq
from ruyaml.representer import RoundTripRepresenter, ScalarNode
from ruyaml.constructor import RoundTripConstructor
from typing import Text, Any, Dict, List  # NOQA


def round_trip_stabler(
    inp,
    outp=None,
):
    if outp is None:
        outp = inp
    doutp = dedent(outp)
    yaml = ruyaml.YAML()
    yaml.preserve_quotes = True
    yaml.preserve_block_seqs_indents = True
    data = yaml.load(doutp)
    buf = io.StringIO()
    yaml.dump(data, stream=buf)
    res = buf.getvalue()
    assert res == doutp


class TestStability:

    def test_blockseq1(self):
        round_trip(
            """
        a:
        - a1
        - a2
        """
        )

    @pytest.mark.xfail(strict=True)
    def test_blockseq2(self):
        round_trip(
            """
        a:
          - a1
          - a2
        """
        )

    @pytest.mark.xfail(strict=True)
    def test_blockseq3(self):
        round_trip(
            """
        a:
          - a1
          - a2
        b:
        - b1
        - b2
        """
        )

class TestStabilityStabler:

    def test_blockseq1(self):
        round_trip_stabler(
            """
        a:
        - a1
        - a2
        """
        )

    def test_blockseq2(self):
        round_trip_stabler(
            """
        a:
          - a1
          - a2
        """
        )

    def test_blockseq3(self):
        round_trip_stabler(
            """
        a:
          - a1
          - a2
        b:
        - b1
        - b2
        """
        )

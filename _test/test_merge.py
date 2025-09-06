"""
testing of anchors and the aliases referring to them
"""

from typing import Any

import pytest  # type: ignore  # NOQA
from roundtrip import (  # type: ignore # NOQA
    YAML,
    dedent,
    round_trip,
    round_trip_dump,
    round_trip_load,
)


def load(s: str) -> Any:
    return round_trip_load(dedent(s))


def compare(d: Any, s: str) -> None:
    assert round_trip_dump(d) == dedent(s)


class TestMerge:
    def test_remove_key_before_merge(self) -> None:
        data = load(
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          g: 5
          h: 6
        """
        )
        del data['d']['f']
        compare(
            data,
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          <<: *aa
          g: 5
          h: 6
        """,
        )

    def test_remove_key_after_merge(self) -> None:
        data = load(
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          g: 5
          h: 6
        """
        )
        del data['d']['g']
        compare(
            data,
            """
        a: &aa
          b: 1
          c: 2
        d:
          e: 3
          f: 4
          <<: *aa
          h: 6
        """,
        )

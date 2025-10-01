# coding: utf-8

import sys
from typing import Any

import pytest  # type: ignore # NOQA
from roundtrip import dedent, round_trip_dump, round_trip_load  # type: ignore

from ruyaml.emitter import Emitter


class TestLeftOverDebug:
    # idea here is to capture round_trip_output via pytest stdout capture
    # if there is are any leftover debug statements they should show up
    def test_00(self, capsys: Any) -> None:
        s = dedent(
            """
        a: 1
        b: []
        c: [a, 1]
        d: {f: 3.14, g: 42}
        """
        )
        d = round_trip_load(s)
        round_trip_dump(d, sys.stdout)
        out, err = capsys.readouterr()
        assert out == s

    def test_01(self, capsys: Any) -> None:
        s = dedent(
            """
        - 1
        - []
        - [a, 1]
        - {f: 3.14, g: 42}
        - - 123
        """
        )
        d = round_trip_load(s)
        round_trip_dump(d, sys.stdout)
        out, err = capsys.readouterr()
        assert out == s

    def test_02(self, capsys: Any) -> None:
        s = dedent(
            """
        - 1
        - { f: 3.14 , g: 42 }
        - {  }
        - [ 3.14 , 42 ]
        - [  ]
        """
        )
        d = round_trip_load(s)

        current_map_start = Emitter.flow_map_start
        current_map_end = Emitter.flow_map_end
        current_map_separator = Emitter.flow_map_separator
        current_seq_start = Emitter.flow_seq_start
        current_seq_end = Emitter.flow_seq_end
        current_seq_separator = Emitter.flow_seq_separator

        Emitter.flow_map_start = '{ '
        Emitter.flow_map_end = ' }'
        Emitter.flow_map_separator = ' ,'

        Emitter.flow_seq_start = '[ '
        Emitter.flow_seq_end = ' ]'
        Emitter.flow_seq_separator = ' ,'

        try:
            round_trip_dump(d, sys.stdout)
        finally:
            Emitter.flow_map_start = current_map_start
            Emitter.flow_map_end = current_map_end
            Emitter.flow_map_separator = current_map_separator

            Emitter.flow_seq_start = current_seq_start
            Emitter.flow_seq_end = current_seq_end
            Emitter.flow_seq_separator = current_seq_separator

        out, err = capsys.readouterr()
        assert out == s

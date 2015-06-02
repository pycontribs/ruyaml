
from __future__ import print_function

import io
import sys
import subprocess

from roundtrip import dedent

from test_util import check_output, call_util


def to_html(s, file_name, mp, td, options=None):
    cmd = ['yaml', 'htmltable', file_name]
    if options:
        cmd.extend(options)
    return call_util(s, file_name, cmd, mp, td)


class TestUtilToHTML:
    def test_html_01(self, tmpdir, monkeypatch):
        file_name = "html.yaml"
        res = to_html(u"""
        - 1
        - 2
        """, file_name, mp=monkeypatch, td=tmpdir, options=["--level"])
        assert res == "levels: 1\n"

    def test_html_02(self, tmpdir, monkeypatch):
        file_name = "html.yaml"
        res = to_html(u"""
        abc:
        - 1
        - 2
        ghi:
        - 3
        - 4
        """, file_name, mp=monkeypatch, td=tmpdir, options=["--level"])
        assert res == "levels: 2\n".format(file_name)

    def test_html_03(self, tmpdir, monkeypatch):
        file_name = "html.yaml"
        res = to_html(u"""
        -
          - 1
          - 2
        -
          - 3
          - 4
        """, file_name, mp=monkeypatch, td=tmpdir, options=["--level"])
        assert res == "levels: 2\n"

    def test_html_03(self, tmpdir, monkeypatch):
        file_name = "html.yaml"
        res = to_html(u"""
        -
          abc:
          - 1
          - 2
          def:
          - 3
          - 4
        """, file_name, mp=monkeypatch, td=tmpdir, options=["--level"])
        assert res == "levels: 3\n"

    def test_html_04(self, tmpdir, monkeypatch):
        file_name = "html.yaml"
        res = to_html(u"""
        title:
        - fruit
        - legume
        local:
        - apple
        - sprouts
        import:
        - orange
        - broccoli
        """, file_name, mp=monkeypatch, td=tmpdir)
        assert res == dedent("""\
        <HTML>
        <HEAD>
        </HEAD>
        <BODY>
        <TABLE>
          <TR>
            <TD>title</TD>
            <TD>fruit</TD>
            <TD>legume</TD>
          </TR>
          <TR>
            <TD>local</TD>
            <TD>apple</TD>
            <TD>sprouts</TD>
          </TR>
          <TR>
            <TD>import</TD>
            <TD>orange</TD>
            <TD>broccoli</TD>
          </TR>
        <TABLE>
        </BODY>
        </HTML>

        """)


from __future__ import print_function

import io
import sys
import subprocess
try:
    _ = subprocess.check_output

    def check_output(*args, **kw):
        try:
            res = subprocess.check_output(*args, **kw)
        except subprocess.CalledProcessError as e:
            print("subprocess.CalledProcessError\n", e.output, sep='')
            res = e.output
        if PY3:
            res = res.decode('utf-8')
        return res
except AttributeError:
    def check_output(*args, **kw):
        process = subprocess.Popen(stdout=subprocess.PIPE, *args, **kw)
        output, unused_err = process.communicate()
        if PY3:
            output = output.decode('utf-8')
        return output

import pytest

import ruamel.yaml
from ruamel.yaml.compat import PY3
from roundtrip import dedent


def call_util(s, file_name, cmd, mp, td):
    """call the utilitiy yaml. if exit != 0 or if somethhing goes wrong
    return error output"""
    mp.chdir(td)
    with io.open(file_name, 'w') as fp:
        fp.write(dedent(s))
    res = check_output(cmd, stderr=subprocess.STDOUT)
    return res.replace('\r\n', '\n')


def rt_test(s, file_name, mp, td):
    return call_util(s, file_name, ['yaml', 'rt', "-v", file_name], mp, td)


class TestUtil:

    def test_version(self, capsys):
        res = check_output(
            ['yaml', '--version'], stderr=subprocess.STDOUT)
        assert res.replace('\r\n', '\n') == \
               u"version: {0}\n".format(ruamel.yaml.__version__)

    def test_ok(self, tmpdir, monkeypatch):
        file_name = "00_ok.yaml"
        res = rt_test(u"""
        - abc
        - ghi  # some comment
        - klm
        """, file_name, mp=monkeypatch, td=tmpdir)
        assert res == "{0}: ok\n".format(file_name)

    def test_not_ok(self, tmpdir, monkeypatch):
        file_name = "01_second_rt_ok.yaml"
        res = rt_test(u"""
        - abc
        -  ghi # some comment
        - klm
        """, file_name, mp=monkeypatch, td=tmpdir)
        assert res.replace('\r\n', '\n') == dedent("""
        {file_name}:
             stabilizes on second round trip, ok without comments
        --- 01_second_rt_ok.yaml
        +++ round trip YAML
        @@ -1,3 +1,3 @@
         - abc
        --  ghi # some comment
        +- ghi  # some comment
         - klm
        """).format(**dict(file_name=file_name))

    def test_from_configobj(self, tmpdir, monkeypatch):
        file_name = "02_from_ini.yaml"
        res = call_util(
            u"""
        # initial comment

        keyword1 = value1
        keyword2 = value2

        [section 1]
        keyword1 = value1
        keyword2 = value2

            [[sub-section]]
            # this is in section 1
            keyword1 = value1
            keyword2 = value2

                [[[nested section]]]
                # this is in sub section
                keyword1 = value1
                keyword2 = value2

            [[sub-section2]]
            # this is in section 1 again
            keyword1 = value1
            keyword2 = value2

        [[sub-section3]]
        # this is also in section 1, indentation is misleading here
        keyword1 = value1
        keyword2 = value2

        # final comment
        """, file_name, ['yaml', 'from-ini', file_name],
            mp=monkeypatch, td=tmpdir)
        print(res)
        assert res.replace('\r\n', '\n') == dedent("""
        # initial comment
        keyword1: value1
        keyword2: value2
        section 1:
          keyword1: value1
          keyword2: value2
          sub-section:
            # this is in section 1
            keyword1: value1
            keyword2: value2
            nested section:
              # this is in sub section
              keyword1: value1
              keyword2: value2
          sub-section2:
            # this is in section 1 again
            keyword1: value1
            keyword2: value2
          sub-section3:
            # this is also in section 1, indentation is misleading here
            keyword1: value1
            keyword2: value2
        # final comment
        """)

    def test_from_configobj_extra_comments(self, tmpdir, monkeypatch):
        file_name = "02_from_ini.yaml"
        res = call_util(
            u"""
        # initial comment
        keyword1 = value1
        keyword2 = value2  # eol comment kw2

        [section 1]
        keyword1 = value1 # and here more comment
        # comment s1kw2
        keyword2 = value2  # eol comment s1kw2

            [[sub-section]]  # eol on section
            # this is in section 1
            keyword1 = value1
            keyword2 = value2

                [[[nested section]]]
                # this is in sub section
                keyword1 = value1
                keyword2 = value2
                # after nested

            [[sub-section2]]
            # this is in section 1 again
            keyword1 = value1
            keyword2 = value2

        [[sub-section3]] # comment on section key
        # this is also in section 1, indentation is misleading here
        keyword1 = value1
        keyword2 = value2

        # final comment
        """,
            file_name, ['yaml', 'from-ini', file_name],
            mp=monkeypatch, td=tmpdir)
        print(res)
        assert res.replace('\r\n', '\n') == dedent("""
        # initial comment
        keyword1: value1
        keyword2: value2 # eol comment kw2
        section 1:
          keyword1: value1 # and here more comment
          # comment s1kw2
          keyword2: value2 # eol comment s1kw2
          sub-section: # eol on section
            # this is in section 1
            keyword1: value1
            keyword2: value2
            nested section:
              # this is in sub section
              keyword1: value1
              keyword2: value2
          # after nested
          sub-section2:
            # this is in section 1 again
            keyword1: value1
            keyword2: value2
          sub-section3: # comment on section key
            # this is also in section 1, indentation is misleading here
            keyword1: value1
            keyword2: value2
        # final comment
        """)

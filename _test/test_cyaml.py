# coding: utf-8

import platform
import sys
from textwrap import dedent

import pytest


@pytest.mark.skipif(
    platform.python_implementation() in ['Jython', 'PyPy'],
    reason='Jython throws RepresenterError',
)
@pytest.mark.xfail(reason="cyaml not ported yet")
def test_load_cyaml():
    print("???????????????????????", platform.python_implementation())
    import ruyaml

    if sys.version_info >= (3, 8):
        return
    assert ruyaml.__with_libyaml__
    from ruyaml.cyaml import CLoader

    ruyaml.load('abc: 1', Loader=CLoader)


@pytest.mark.skipif(
    sys.version_info >= (3, 8)
    or platform.python_implementation() in ['Jython', 'PyPy'],
    reason='no _PyGC_FINALIZED',
)
@pytest.mark.xfail(reason="cyaml not ported yet")
def test_dump_cyaml():
    import ruyaml

    if sys.version_info >= (3, 8):
        return
    data = {'a': 1, 'b': 2}
    res = ruyaml.dump(
        data,
        Dumper=ruyaml.cyaml.CSafeDumper,
        default_flow_style=False,
        allow_unicode=True,
    )
    assert res == 'a: 1\nb: 2\n'


@pytest.mark.skipif(
    platform.python_implementation() in ['Jython', 'PyPy'], reason='not avialable'
)
@pytest.mark.xfail(reason="cyaml not ported yet")
def test_load_cyaml_1_2():
    # issue 155
    import ruyaml

    if sys.version_info >= (3, 8):
        return
    assert ruyaml.__with_libyaml__
    inp = dedent(
        """\
    %YAML 1.2
    ---
    num_epochs: 70000
    """
    )
    yaml = ruyaml.YAML(typ='safe')
    yaml.load(inp)


@pytest.mark.skipif(
    platform.python_implementation() in ['Jython', 'PyPy'], reason='not available'
)
@pytest.mark.xfail(reason="cyaml not ported yet")
def test_dump_cyaml_1_2():
    # issue 155
    from io import StringIO

    import ruyaml

    if sys.version_info >= (3, 8):
        return
    assert ruyaml.__with_libyaml__
    yaml = ruyaml.YAML(typ='safe')
    yaml.version = (1, 2)
    yaml.default_flow_style = False
    data = {'a': 1, 'b': 2}
    exp = dedent(
        """\
    %YAML 1.2
    ---
    a: 1
    b: 2
    """
    )
    buf = StringIO()
    yaml.dump(data, buf)
    assert buf.getvalue() == exp

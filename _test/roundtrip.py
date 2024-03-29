# coding: utf-8

"""
helper routines for testing round trip of commented YAML data
"""
import io
import sys
import textwrap
from pathlib import Path

import ruyaml

unset = object()


def dedent(data):
    try:
        position_of_first_newline = data.index('\n')
        for idx in range(position_of_first_newline):
            if not data[idx].isspace():
                raise ValueError
    except ValueError:
        pass
    else:
        data = data[position_of_first_newline + 1 :]
    return textwrap.dedent(data)


def round_trip_load(inp, preserve_quotes=None, version=None):
    import ruyaml  # NOQA

    dinp = dedent(inp)
    yaml = ruyaml.YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.version = version
    return yaml.load(dinp)


def round_trip_load_all(inp, preserve_quotes=None, version=None):
    import ruyaml  # NOQA

    dinp = dedent(inp)
    yaml = ruyaml.YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.version = version
    return yaml.load_all(dinp)


def round_trip_dump(
    data,
    stream=None,  # *,
    indent=None,
    block_seq_indent=None,
    default_flow_style=unset,
    top_level_colon_align=None,
    prefix_colon=None,
    explicit_start=None,
    explicit_end=None,
    version=None,
    allow_unicode=True,
):
    import ruyaml  # NOQA

    yaml = ruyaml.YAML()
    yaml.indent(mapping=indent, sequence=indent, offset=block_seq_indent)
    if default_flow_style is not unset:
        yaml.default_flow_style = default_flow_style
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    yaml.version = version
    yaml.allow_unicode = allow_unicode
    if stream is not None:
        yaml.dump(data, stream=stream)
        return
    buf = io.StringIO()
    yaml.dump(data, stream=buf)
    return buf.getvalue()


def round_trip_dump_all(
    data,
    stream=None,  # *,
    indent=None,
    block_seq_indent=None,
    default_flow_style=unset,
    top_level_colon_align=None,
    prefix_colon=None,
    explicit_start=None,
    explicit_end=None,
    version=None,
    allow_unicode=None,
):
    yaml = ruyaml.YAML()
    yaml.indent(mapping=indent, sequence=indent, offset=block_seq_indent)
    if default_flow_style is not unset:
        yaml.default_flow_style = default_flow_style
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    yaml.version = version
    yaml.allow_unicode = allow_unicode
    if stream is not None:
        yaml.dump(data, stream=stream)
        return
    buf = io.StringIO()
    yaml.dump_all(data, stream=buf)
    return buf.getvalue()


def diff(inp, outp, file_name='stdin'):
    import difflib

    inl = inp.splitlines(True)  # True for keepends
    outl = outp.splitlines(True)
    diff = difflib.unified_diff(inl, outl, file_name, 'round trip YAML')
    for line in diff:
        sys.stdout.write(line)


def round_trip(
    inp,
    outp=None,
    extra=None,
    intermediate=None,
    indent=None,
    block_seq_indent=None,
    top_level_colon_align=None,
    prefix_colon=None,
    preserve_quotes=None,
    explicit_start=None,
    explicit_end=None,
    version=None,
    dump_data=None,
):
    """
    inp:    input string to parse
    outp:   expected output (equals input if not specified)
    """
    if outp is None:
        outp = inp
    doutp = dedent(outp)
    if extra is not None:
        doutp += extra
    data = round_trip_load(inp, preserve_quotes=preserve_quotes)
    if dump_data:
        print('data', data)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    res = round_trip_dump(
        data,
        indent=indent,
        block_seq_indent=block_seq_indent,
        top_level_colon_align=top_level_colon_align,
        prefix_colon=prefix_colon,
        explicit_start=explicit_start,
        explicit_end=explicit_end,
        version=version,
    )
    if res != doutp:
        diff(doutp, res, 'input string')
    print('\nroundtrip data:\n', res, sep="")
    assert res == doutp
    res = round_trip_dump(
        data,
        indent=indent,
        block_seq_indent=block_seq_indent,
        top_level_colon_align=top_level_colon_align,
        prefix_colon=prefix_colon,
        explicit_start=explicit_start,
        explicit_end=explicit_end,
        version=version,
    )
    print('roundtrip second round data:\n', res, sep="")
    assert res == doutp
    return data


def na_round_trip(
    inp,
    outp=None,
    extra=None,
    intermediate=None,
    indent=None,
    top_level_colon_align=None,
    prefix_colon=None,
    preserve_quotes=None,
    explicit_start=None,
    explicit_end=None,
    version=None,
    dump_data=None,
):
    """
    inp:    input string to parse
    outp:   expected output (equals input if not specified)
    """
    inp = dedent(inp)
    if outp is None:
        outp = inp
    if version is not None:
        version = version
    doutp = dedent(outp)
    if extra is not None:
        doutp += extra
    yaml = YAML()
    yaml.preserve_quotes = preserve_quotes
    yaml.scalar_after_indicator = False  # newline after every directives end
    data = yaml.load(inp)
    if dump_data:
        print('data', data)
    if intermediate is not None:
        if isinstance(intermediate, dict):
            for k, v in intermediate.items():
                if data[k] != v:
                    print('{0!r} <> {1!r}'.format(data[k], v))
                    raise ValueError
    yaml.indent = indent
    yaml.top_level_colon_align = top_level_colon_align
    yaml.prefix_colon = prefix_colon
    yaml.explicit_start = explicit_start
    yaml.explicit_end = explicit_end
    res = yaml.dump(data, compare=doutp)
    return res


def YAML(**kw):
    import ruyaml  # NOQA

    class MyYAML(ruyaml.YAML):
        """auto dedent string parameters on load"""

        def load(self, stream):
            if isinstance(stream, str):
                if stream and stream[0] == '\n':
                    stream = stream[1:]
                stream = textwrap.dedent(stream)
            return ruyaml.YAML.load(self, stream)

        def load_all(self, stream):
            if isinstance(stream, str):
                if stream and stream[0] == '\n':
                    stream = stream[1:]
                stream = textwrap.dedent(stream)
            for d in ruyaml.YAML.load_all(self, stream):
                yield d

        def dump(self, data, **kw):
            from io import BytesIO, StringIO  # NOQA

            assert ('stream' in kw) ^ ('compare' in kw)
            if 'stream' in kw:
                return ruyaml.YAML.dump(data, **kw)
            lkw = kw.copy()
            expected = textwrap.dedent(lkw.pop('compare'))
            unordered_lines = lkw.pop('unordered_lines', False)
            if expected and expected[0] == '\n':
                expected = expected[1:]
            lkw['stream'] = st = StringIO()
            ruyaml.YAML.dump(self, data, **lkw)
            res = st.getvalue()
            print(res)
            if unordered_lines:
                res = sorted(res.splitlines())
                expected = sorted(expected.splitlines())
            assert res == expected

        def round_trip(self, stream, **kw):
            from io import BytesIO, StringIO  # NOQA

            assert isinstance(stream, str)
            lkw = kw.copy()
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
            data = ruyaml.YAML.load(self, stream)
            outp = lkw.pop('outp', stream)
            lkw['stream'] = st = StringIO()
            ruyaml.YAML.dump(self, data, **lkw)
            res = st.getvalue()
            if res != outp:
                diff(outp, res, 'input string')
            assert res == outp

        def round_trip_all(self, stream, **kw):
            from io import BytesIO, StringIO  # NOQA

            assert isinstance(stream, str)
            lkw = kw.copy()
            if stream and stream[0] == '\n':
                stream = stream[1:]
            stream = textwrap.dedent(stream)
            data = list(ruyaml.YAML.load_all(self, stream))
            outp = lkw.pop('outp', stream)
            lkw['stream'] = st = StringIO()
            ruyaml.YAML.dump_all(self, data, **lkw)
            res = st.getvalue()
            if res != outp:
                diff(outp, res, 'input string')
            assert res == outp

    return MyYAML(**kw)


def save_and_run(program, base_dir=None, output=None, file_name=None, optimized=False):
    """
    safe and run a python program, thereby circumventing any restrictions on module level
    imports
    """
    from subprocess import STDOUT, CalledProcessError, check_output

    if not hasattr(base_dir, 'hash'):
        base_dir = Path(str(base_dir))
    if file_name is None:
        file_name = 'safe_and_run_tmp.py'
    file_name = base_dir / file_name
    file_name.write_text(dedent(program))

    try:
        cmd = [sys.executable, '-Wd']
        if optimized:
            cmd.append('-O')
        cmd.append(str(file_name))
        print('running:', *cmd)
        # 3.5 needs strings
        res = check_output(
            cmd, stderr=STDOUT, universal_newlines=True, cwd=str(base_dir)
        )
        if output is not None:
            if '__pypy__' in sys.builtin_module_names:
                res = res.splitlines(True)
                res = [line for line in res if 'no version info' not in line]
                res = ''.join(res)
            print('result:  ', res, end='')
            print('expected:', output, end='')
            assert res == output
    except CalledProcessError as exception:
        print("##### Running '{} {}' FAILED #####".format(sys.executable, file_name))
        print(exception.output)
        return exception.returncode
    return 0

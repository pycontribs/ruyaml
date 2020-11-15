# coding: utf-8

from __future__ import absolute_import, print_function

import pprint
import types

import _ruyaml

import ruyaml

ruyaml.PyBaseLoader = ruyaml.BaseLoader
ruyaml.PySafeLoader = ruyaml.SafeLoader
ruyaml.PyLoader = ruyaml.Loader
ruyaml.PyBaseDumper = ruyaml.BaseDumper
ruyaml.PySafeDumper = ruyaml.SafeDumper
ruyaml.PyDumper = ruyaml.Dumper

old_scan = ruyaml.scan


def new_scan(stream, Loader=ruyaml.CLoader):
    return old_scan(stream, Loader)


old_parse = ruyaml.parse


def new_parse(stream, Loader=ruyaml.CLoader):
    return old_parse(stream, Loader)


old_compose = ruyaml.compose


def new_compose(stream, Loader=ruyaml.CLoader):
    return old_compose(stream, Loader)


old_compose_all = ruyaml.compose_all


def new_compose_all(stream, Loader=ruyaml.CLoader):
    return old_compose_all(stream, Loader)


old_load = ruyaml.load


def new_load(stream, Loader=ruyaml.CLoader):
    return old_load(stream, Loader)


old_load_all = ruyaml.load_all


def new_load_all(stream, Loader=ruyaml.CLoader):
    return old_load_all(stream, Loader)


old_safe_load = ruyaml.safe_load


def new_safe_load(stream):
    return old_load(stream, ruyaml.CSafeLoader)


old_safe_load_all = ruyaml.safe_load_all


def new_safe_load_all(stream):
    return old_load_all(stream, ruyaml.CSafeLoader)


old_emit = ruyaml.emit


def new_emit(events, stream=None, Dumper=ruyaml.CDumper, **kwds):
    return old_emit(events, stream, Dumper, **kwds)


old_serialize = ruyaml.serialize


def new_serialize(node, stream, Dumper=ruyaml.CDumper, **kwds):
    return old_serialize(node, stream, Dumper, **kwds)


old_serialize_all = ruyaml.serialize_all


def new_serialize_all(nodes, stream=None, Dumper=ruyaml.CDumper, **kwds):
    return old_serialize_all(nodes, stream, Dumper, **kwds)


old_dump = ruyaml.dump


def new_dump(data, stream=None, Dumper=ruyaml.CDumper, **kwds):
    return old_dump(data, stream, Dumper, **kwds)


old_dump_all = ruyaml.dump_all


def new_dump_all(documents, stream=None, Dumper=ruyaml.CDumper, **kwds):
    return old_dump_all(documents, stream, Dumper, **kwds)


old_safe_dump = ruyaml.safe_dump


def new_safe_dump(data, stream=None, **kwds):
    return old_dump(data, stream, ruyaml.CSafeDumper, **kwds)


old_safe_dump_all = ruyaml.safe_dump_all


def new_safe_dump_all(documents, stream=None, **kwds):
    return old_dump_all(documents, stream, ruyaml.CSafeDumper, **kwds)


def _set_up():
    ruyaml.BaseLoader = ruyaml.CBaseLoader
    ruyaml.SafeLoader = ruyaml.CSafeLoader
    ruyaml.Loader = ruyaml.CLoader
    ruyaml.BaseDumper = ruyaml.CBaseDumper
    ruyaml.SafeDumper = ruyaml.CSafeDumper
    ruyaml.Dumper = ruyaml.CDumper
    ruyaml.scan = new_scan
    ruyaml.parse = new_parse
    ruyaml.compose = new_compose
    ruyaml.compose_all = new_compose_all
    ruyaml.load = new_load
    ruyaml.load_all = new_load_all
    ruyaml.safe_load = new_safe_load
    ruyaml.safe_load_all = new_safe_load_all
    ruyaml.emit = new_emit
    ruyaml.serialize = new_serialize
    ruyaml.serialize_all = new_serialize_all
    ruyaml.dump = new_dump
    ruyaml.dump_all = new_dump_all
    ruyaml.safe_dump = new_safe_dump
    ruyaml.safe_dump_all = new_safe_dump_all


def _tear_down():
    ruyaml.BaseLoader = ruyaml.PyBaseLoader
    ruyaml.SafeLoader = ruyaml.PySafeLoader
    ruyaml.Loader = ruyaml.PyLoader
    ruyaml.BaseDumper = ruyaml.PyBaseDumper
    ruyaml.SafeDumper = ruyaml.PySafeDumper
    ruyaml.Dumper = ruyaml.PyDumper
    ruyaml.scan = old_scan
    ruyaml.parse = old_parse
    ruyaml.compose = old_compose
    ruyaml.compose_all = old_compose_all
    ruyaml.load = old_load
    ruyaml.load_all = old_load_all
    ruyaml.safe_load = old_safe_load
    ruyaml.safe_load_all = old_safe_load_all
    ruyaml.emit = old_emit
    ruyaml.serialize = old_serialize
    ruyaml.serialize_all = old_serialize_all
    ruyaml.dump = old_dump
    ruyaml.dump_all = old_dump_all
    ruyaml.safe_dump = old_safe_dump
    ruyaml.safe_dump_all = old_safe_dump_all


def test_c_version(verbose=False):
    if verbose:
        print(_ruyaml.get_version())
        print(_ruyaml.get_version_string())
    assert ('%s.%s.%s' % _ruyaml.get_version()) == _ruyaml.get_version_string(), (
        _ruyaml.get_version(),
        _ruyaml.get_version_string(),
    )


def _compare_scanners(py_data, c_data, verbose):
    py_tokens = list(ruyaml.scan(py_data, Loader=ruyaml.PyLoader))
    c_tokens = []
    try:
        for token in ruyaml.scan(c_data, Loader=ruyaml.CLoader):
            c_tokens.append(token)
        assert len(py_tokens) == len(c_tokens), (len(py_tokens), len(c_tokens))
        for py_token, c_token in zip(py_tokens, c_tokens):
            assert py_token.__class__ == c_token.__class__, (py_token, c_token)
            if hasattr(py_token, 'value'):
                assert py_token.value == c_token.value, (py_token, c_token)
            if isinstance(py_token, ruyaml.StreamEndToken):
                continue
            py_start = (
                py_token.start_mark.index,
                py_token.start_mark.line,
                py_token.start_mark.column,
            )
            py_end = (
                py_token.end_mark.index,
                py_token.end_mark.line,
                py_token.end_mark.column,
            )
            c_start = (
                c_token.start_mark.index,
                c_token.start_mark.line,
                c_token.start_mark.column,
            )
            c_end = (
                c_token.end_mark.index,
                c_token.end_mark.line,
                c_token.end_mark.column,
            )
            assert py_start == c_start, (py_start, c_start)
            assert py_end == c_end, (py_end, c_end)
    finally:
        if verbose:
            print('PY_TOKENS:')
            pprint.pprint(py_tokens)
            print('C_TOKENS:')
            pprint.pprint(c_tokens)


def test_c_scanner(data_filename, canonical_filename, verbose=False):
    with open(data_filename, 'rb') as fp0:
        with open(data_filename, 'rb') as fp1:
            _compare_scanners(fp0, fp1, verbose)
    with open(data_filename, 'rb') as fp0:
        with open(data_filename, 'rb') as fp1:
            _compare_scanners(fp0.read(), fp1.read(), verbose)
    with open(canonical_filename, 'rb') as fp0:
        with open(canonical_filename, 'rb') as fp1:
            _compare_scanners(fp0, fp1, verbose)
    with open(canonical_filename, 'rb') as fp0:
        with open(canonical_filename, 'rb') as fp1:
            _compare_scanners(fp0.read(), fp1.read(), verbose)


test_c_scanner.unittest = ['.data', '.canonical']
test_c_scanner.skip = ['.skip-ext']


def _compare_parsers(py_data, c_data, verbose):
    py_events = list(ruyaml.parse(py_data, Loader=ruyaml.PyLoader))
    c_events = []
    try:
        for event in ruyaml.parse(c_data, Loader=ruyaml.CLoader):
            c_events.append(event)
        assert len(py_events) == len(c_events), (len(py_events), len(c_events))
        for py_event, c_event in zip(py_events, c_events):
            for attribute in [
                '__class__',
                'anchor',
                'tag',
                'implicit',
                'value',
                'explicit',
                'version',
                'tags',
            ]:
                py_value = getattr(py_event, attribute, None)
                c_value = getattr(c_event, attribute, None)
                assert py_value == c_value, (py_event, c_event, attribute)
    finally:
        if verbose:
            print('PY_EVENTS:')
            pprint.pprint(py_events)
            print('C_EVENTS:')
            pprint.pprint(c_events)


def test_c_parser(data_filename, canonical_filename, verbose=False):
    with open(data_filename, 'rb') as fp0:
        with open(data_filename, 'rb') as fp1:
            _compare_parsers(fp0, fp1, verbose)
    with open(data_filename, 'rb') as fp0:
        with open(data_filename, 'rb') as fp1:
            _compare_parsers(fp0.read(), fp1.read(), verbose)
    with open(canonical_filename, 'rb') as fp0:
        with open(canonical_filename, 'rb') as fp1:
            _compare_parsers(fp0, fp1, verbose)
    with open(canonical_filename, 'rb') as fp0:
        with open(canonical_filename, 'rb') as fp1:
            _compare_parsers(fp0.read(), fp1.read(), verbose)


test_c_parser.unittest = ['.data', '.canonical']
test_c_parser.skip = ['.skip-ext']


def _compare_emitters(data, verbose):
    events = list(ruyaml.parse(data, Loader=ruyaml.PyLoader))
    c_data = ruyaml.emit(events, Dumper=ruyaml.CDumper)
    if verbose:
        print(c_data)
    py_events = list(ruyaml.parse(c_data, Loader=ruyaml.PyLoader))
    c_events = list(ruyaml.parse(c_data, Loader=ruyaml.CLoader))
    try:
        assert len(events) == len(py_events), (len(events), len(py_events))
        assert len(events) == len(c_events), (len(events), len(c_events))
        for event, py_event, c_event in zip(events, py_events, c_events):
            for attribute in [
                '__class__',
                'anchor',
                'tag',
                'implicit',
                'value',
                'explicit',
                'version',
                'tags',
            ]:
                value = getattr(event, attribute, None)
                py_value = getattr(py_event, attribute, None)
                c_value = getattr(c_event, attribute, None)
                if (
                    attribute == 'tag'
                    and value in [None, u'!']
                    and py_value in [None, u'!']
                    and c_value in [None, u'!']
                ):
                    continue
                if attribute == 'explicit' and (py_value or c_value):
                    continue
                assert value == py_value, (event, py_event, attribute)
                assert value == c_value, (event, c_event, attribute)
    finally:
        if verbose:
            print('EVENTS:')
            pprint.pprint(events)
            print('PY_EVENTS:')
            pprint.pprint(py_events)
            print('C_EVENTS:')
            pprint.pprint(c_events)


def test_c_emitter(data_filename, canonical_filename, verbose=False):
    with open(data_filename, 'rb') as fp0:
        _compare_emitters(fp0.read(), verbose)
    with open(canonical_filename, 'rb') as fp0:
        _compare_emitters(fp0.read(), verbose)


test_c_emitter.unittest = ['.data', '.canonical']
test_c_emitter.skip = ['.skip-ext']


def wrap_ext_function(function):
    def wrapper(*args, **kwds):
        _set_up()
        try:
            function(*args, **kwds)
        finally:
            _tear_down()

    wrapper.__name__ = '%s_ext' % function.__name__
    wrapper.unittest = function.unittest
    wrapper.skip = getattr(function, 'skip', []) + ['.skip-ext']
    return wrapper


def wrap_ext(collections):
    functions = []
    if not isinstance(collections, list):
        collections = [collections]
    for collection in collections:
        if not isinstance(collection, dict):
            collection = vars(collection)
        for key in sorted(collection):
            value = collection[key]
            if isinstance(value, types.FunctionType) and hasattr(value, 'unittest'):
                functions.append(wrap_ext_function(value))
    for function in functions:
        assert function.__name__ not in globals()
        globals()[function.__name__] = function


import test_constructor  # NOQA
import test_emitter  # NOQA
import test_errors  # NOQA
import test_input_output  # NOQA
import test_recursive  # NOQA
import test_representer  # NOQA
import test_resolver  # NOQA
import test_structure  # NOQA
import test_tokens  # NOQA

wrap_ext(
    [
        test_tokens,
        test_structure,
        test_errors,
        test_resolver,
        test_constructor,
        test_emitter,
        test_representer,
        test_recursive,
        test_input_output,
    ]
)

if __name__ == '__main__':
    import sys

    import test_appliance

    sys.exit(test_appliance.run(globals()))

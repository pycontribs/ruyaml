# from __future__ import absolute_import
from __future__ import print_function

import canonical  # NOQA

import ruyaml


def test_canonical_scanner(canonical_filename, verbose=False):
    with open(canonical_filename, 'rb') as fp0:
        data = fp0.read()
    tokens = list(ruyaml.canonical_scan(data))
    assert tokens, tokens
    if verbose:
        for token in tokens:
            print(token)


test_canonical_scanner.unittest = ['.canonical']


def test_canonical_parser(canonical_filename, verbose=False):
    with open(canonical_filename, 'rb') as fp0:
        data = fp0.read()
    events = list(ruyaml.canonical_parse(data))
    assert events, events
    if verbose:
        for event in events:
            print(event)


test_canonical_parser.unittest = ['.canonical']


def test_canonical_error(data_filename, canonical_filename, verbose=False):
    with open(data_filename, 'rb') as fp0:
        data = fp0.read()
    try:
        output = list(ruyaml.canonical_load_all(data))  # NOQA
    except ruyaml.YAMLError as exc:
        if verbose:
            print(exc)
    else:
        raise AssertionError('expected an exception')


test_canonical_error.unittest = ['.data', '.canonical']
test_canonical_error.skip = ['.empty']

if __name__ == '__main__':
    import test_appliance

    test_appliance.run(globals())

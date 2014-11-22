from __future__ import absolute_import
from __future__ import print_function

import codecs
import io

from ruamel.yaml.py.compat import PY2
import ruamel.yaml.py.reader

def _run_reader(data, verbose):
    try:
        stream = ruamel.yaml.py.reader.Reader(data)
        while stream.peek() != u'\0':
            stream.forward()
    except ruamel.yaml.py.reader.ReaderError as exc:
        if verbose:
            print(exc)
    else:
        raise AssertionError("expected an exception")

def test_stream_error(error_filename, verbose=False):
    _run_reader(open(error_filename, 'rb'), verbose)
    _run_reader(open(error_filename, 'rb').read(), verbose)
    for encoding in ['utf-8', 'utf-16-le', 'utf-16-be']:
        try:
            if PY2:
                data = unicode(open(error_filename, 'rb').read(), encoding)
            else:
                data = open(error_filename, 'rb').read().decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        return
    _run_reader(data, verbose)
    _run_reader(io.open(error_filename, encoding=encoding), verbose)

test_stream_error.unittest = ['.stream-error']

if __name__ == '__main__':
    import test_appliance
    test_appliance.run(globals())


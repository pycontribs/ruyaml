

"""
helper routines for testing round trip of commented YAML data
"""
import textwrap
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import ruamel.yaml
from ruamel.yaml import RoundTripLoader
from ruamel.yaml import RoundTripDumper


def dedent(data):
    try:
        position_of_first_newline = data.index('\n')
        for idx in range(position_of_first_newline):
            if not data[idx].isspace():
                raise ValueError
    except ValueError:
        pass
    else:
        data = data[position_of_first_newline+1:]
    return textwrap.dedent(data)


def round_trip_load(dinp):
    return ruamel.yaml.load(dinp, RoundTripLoader)


def round_trip_dump(data):
    stream = StringIO()
    dumper = RoundTripDumper
    return ruamel.yaml.dump(data, default_flow_style=False, Dumper=dumper)


def round_trip(inp, outp=None, extra=None):
    dinp = dedent(inp)
    if outp is not None:
        doutp = dedent(outp)
    else:
        doutp = dinp
    if extra is not None:
        doutp += extra
    data = round_trip_load(dinp)
    assert round_trip_dump(data) == doutp

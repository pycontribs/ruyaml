
# partially from package six by Benjamin Peterson

import sys
import types

try:
    from ruamel.ordereddict import ordereddict
except:
    try:
        from collections import OrderedDict
    except ImportError:
        from orderddict import OrderedDict
    # to get the right name import ... as ordereddict doesn't do that

    class ordereddict(OrderedDict):
        pass

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    def utf8(s):
        return s

    def to_str(s):
        return s

    def to_unicode(s):
        return s

else:
    def utf8(s):
        return s.encode('utf-8')

    def to_str(s):
        return str(s)

    def to_unicode(s):
        return unicode(s)

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
    unichr = chr
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO

else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    unichr = unichr  # to allow importing
    import StringIO
    StringIO = StringIO.StringIO
    import cStringIO
    BytesIO = cStringIO.StringIO

if PY3:
    builtins_module = 'builtins'
else:
    builtins_module = '__builtin__'


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})

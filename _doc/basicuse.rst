***********
Basic Usage
***********

You load a YAML document using:
--- !python |
from ruyaml import YAML

    from ruyaml import YAML

    yaml=YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
    yaml.load(doc)

in this ``doc`` can be a file pointer (i.e. an object that has the
``.read()`` method, a string or a ``pathlib.Path()``. ``typ='safe'``
accomplishes the same as what ``safe_load()`` did before: loading of a
document without resolving unknown tags. Provide  ``pure=True`` to
enforce using the pure Python implementation, otherwise the faster C libraries will be used
when possible/available but these behave slightly different (and sometimes more like a YAML 1.1 loader).

Dumping works in the same way::

    from ruyaml import YAML

    yaml=YAML()
    yaml.default_flow_style = False
    yaml.dump({'a': [1, 2]}, s)

in this ``s`` can be a file pointer (i.e. an object that has the
``.write()`` method, or a ``pathlib.Path()``. If you want to display
your output, just stream to ``sys.stdout``.

If you need to transform a string representation of the output provide
a function that takes a string as input and returns one:

    def tr(s):
        return s.replace('\n', '<\n')  # such output is not valid YAML!

    yaml.dump(data, sys.stdout, transform=tr)

More examples
=============

Using the C based SafeLoader (at this time is inherited from
libyaml/PyYAML and e.g. loads ``0o52`` as well as ``052`` load as integer ``42``):

    from ruyaml import YAML

    yaml=YAML(typ="safe")
    yaml.load("""a:\n  b: 2\n  c: 3\n""")

--- |
Using the Python based SafeLoader (YAML 1.2 support, ``052`` loads as ``52``):
--- !python |

    from ruyaml import YAML

    yaml=YAML(typ="safe", pure=True)
    yaml.load("""a:\n  b: 2\n  c: 3\n""")

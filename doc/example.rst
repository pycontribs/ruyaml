********
Examples
********

Basic round trip of parsing YAML to Python objects, modifying
and generating YAML::

  import sys
  from ruamel.yaml import YAML

  inp = """\
  # example
  name:
    # details
    family: Smith   # very common
    given: Alice    # one of the siblings
  """

  yaml = YAML()
  code = yaml.load(inp)
  code['name']['given'] = 'Bob'

  yaml.dump(code, sys.stdout)

Resulting in::

  # example
  name:
    # details
    family: Smith   # very common
    given: Bob      # one of the siblings

with the old API::

  from __future__ import print_function

  import sys
  import ruamel.yaml

  inp = """\
  # example
  name:
    # details
    family: Smith   # very common
    given: Alice    # one of the siblings
  """

  code = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)
  code['name']['given'] = 'Bob'

  ruamel.yaml.dump(code, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)

  # the last statement can be done less efficient in time and memory with
  # leaving out the end='' would cause a double newline at the end
  # print(ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper), end='')

Resulting in ::

  # example
  name:
    # details
    family: Smith   # very common
    given: Bob      # one of the siblings

----

YAML handcrafted anchors and references as well as key merging
are preserved. The merged keys can transparently be accessed
using ``[]`` and ``.get()``::

  from ruamel.yaml import YAML

  inp = """\
  - &CENTER {x: 1, y: 2}
  - &LEFT {x: 0, y: 2}
  - &BIG {r: 10}
  - &SMALL {r: 1}
  # All the following maps are equal:
  # Explicit keys
  - x: 1
    y: 2
    r: 10
    label: center/big
  # Merge one map
  - <<: *CENTER
    r: 10
    label: center/big
  # Merge multiple maps
  - <<: [*CENTER, *BIG]
    label: center/big
  # Override
  - <<: [*BIG, *LEFT, *SMALL]
    x: 1
    label: center/big
  """

  yaml = YAML()
  data = yaml.load(inp)
  assert data[7]['y'] == 2


The ``CommentedMap``, which is the ``dict`` like construct one gets when round-trip loading,
supports insertion of a key into a particular position, while optionally adding a comment::

  import sys
  from ruamel.yaml import YAML

  yaml_str = """\
  first_name: Art
  occupation: Architect  # This is an occupation comment
  about: Art Vandelay is a fictional character that George invents...
  """

  yaml = YAML()
  data = yaml.load(yaml_str)
  data.insert(1, 'last name', 'Vandelay', comment="new key")
  yaml.dump(data, sys.stdout)

gives::

  first_name: Art
  last name: Vandelay    # new key
  occupation: Architect  # This is an occupation comment
  about: Art Vandelay is a fictional character that George invents...

Please note that the comment is aligned with that of its neighbour (if available).

The above was inspired by a `question <http://stackoverflow.com/a/36970608/1307905>`_
posted by *demux* on StackOverflow.

----

By default ``ruamel.yaml`` indents with two positions in block style, for
both mappings and sequences. For sequences the indent is counted to the
beginning of the scalar, with the dash taking the first position of the
indented "space".

You can change this default indentation by e.g. using ``yaml.indent()``::

  import sys
  from ruamel.yaml import YAML

  d = dict(a=dict(b=2),c=[3, 4])
  yaml = YAML()
  yaml.dump(d, sys.stdout)
  print('0123456789')
  yaml = YAML()
  yaml.indent(mapping=4, sequence=6, offset=3)
  yaml.dump(d, sys.stdout)
  print('0123456789')


giving::

  a:
    b: 2
  c:
  - 3
  - 4
  0123456789
  a:
      b: 2
  c:
     -  3
     -  4
  0123456789


If a block sequence or block mapping is the element of a sequence, the
are, by default, displayed `compact
<http://yaml.org/spec/1.2/spec.html#id2797686>`__ notation. This means
that the dash of the "parent" sequence is on the same line as the
first element resp. first key/value pair of the child collection.

If you want either or both of these (sequence within sequence, mapping
within sequence) to begin on the next line use ``yaml.compact()``::

  import sys
  from ruamel.yaml import YAML

  d = [dict(b=2), [3, 4]]
  yaml = YAML()
  yaml.dump(d, sys.stdout)
  print('='*15)
  yaml = YAML()
  yaml.compact(seq_seq=False, seq_map=False)
  yaml.dump(d, sys.stdout)


ruamel.yaml
===========

``ruamel.yaml`` is a YAML package for Python. It is a derivative
of Kirill Simonov's `PyYAML 3.11 <https://bitbucket.org/xi/pyyaml>`_
which supports YAML1.1

Major differences with PyYAML 3.11:

- intergrated Python 2 and 3 sources, running on Python 2.6, 2.7, 3.3 and 3.4.
- round trip mode that **includes comments** (block mode, key ordering kept)
- support for simple lists as mapping keys by transformation to tuples
- ``!!omap`` generates ordereddict (C) on Python 2, collections.OrderedDict
  on Python 3, and ``!!omap`` is generated for these types.
- some YAML 1.2 enhancements (``0o`` octal prefix, ``\/`` escape)
- pep8 compliance
- tox and py.test based testing
- currently assumes that the C yaml library is installed as well as the header
  files. That library
  doesn't generate CommentTokens, so it cannot be used to do
  round trip editing on comments. It can be used for speeded up normal
  processing (so you don't need to install ``ruamel.yaml`` and ``PyYaml``).
  See the section *Requirements*.


Round trip including comments
=============================

The major motivation for this fork is the round-trip capability for
comments. The integration of the sources was just an initial step to
make this easier.

Config file formats
-------------------

There are only a few configuration file formats that are human
readable and editable: JSON, INI/ConfigParser, YAML (XML is to verbose
to be readable).

Unfortunately `JSON <http://www.json.org/>`_ doesn't support comments,
and although there are some solutions with pre-processed filtering of
comments, there are no libraries that support round trip updating of
such commented files.

INI files support comments, and the excellent `ConfigObj
<http://www.voidspace.org.uk/python/configobj.html>`_ library by Foord
and Larosa even supports round trip editing with comment preservation,
nesting of sections and limited lists (within a value). Retrieval of
particular value format is explicit (and extensible).

YAML has basic mapping and sequence structures as well support for
ordered mappings and sets. It supports scalars are of various types
including dates and datetimes (missing in JSON) as a list of
YAML has comments, but these are normally thrown away.

Block structured YAML is a clean and very human readable
format. By extending the Python YAML parser to support round trip
preservation of comments, it makes YAML a very good choice for
configuration files that are human readable and editable while at
the same time interpretable and modifiable by a program.

Examples
========

Basic round trip of parsing YAML to Python objects, modifying
and generating YAML::

  from __future__ import print_function

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

  print(ruamel.yaml.dump(code, Dumper= ruamel.yaml.RoundTripDumper), end='')

.. example code small.py

Resulting in ::

  # example
  name:
    # details
    family: Smith   # very common
    given: Bob      # one of the siblings


.. example output small.py

Requirements
============

You currently have to have the C yaml library and headers installed, as well as
the header files for your Python executables.

On Debian systems you should use::

    sudo apt-get install libyaml-dev python-dev python3-dev

you can leave out ``python3-dev`` if you don't use python3

For CentOS (7) based systems you should do::

   sudo yum install libyaml-devel python-devel

Testing
=======

Testing is done using the `tox <https://pypi.python.org/pypi/tox>`_, which
uses `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ and
`pytest <http://pytest.org/latest/>`_.


yaml utlity
===========

A utility name  ``yaml`` is included and allows for basic operations on files:

- ``yaml round-trip <file_name>`` for basic roundtrip testing of YAML
  files
- ``yaml json <file_name>`` for conversion of JSON file(s) to a single
  YAML block style document
- ``yaml ini <file_name>`` for conversion of an INI/config file (ConfigObj
  comment and nested sections supported) to a YAML block style document

See ``yaml --help`` for more information on the availble commands

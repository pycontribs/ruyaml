
ruamel.yaml
===========

``ruamel.yaml`` is a YAML package for Python. It is a derivative
of Kirill Simonov's `PyYAML 3.11 <https://bitbucket.org/xi/pyyaml>`_
which is a YAML1.1 

Major differences with PyYAML 3.11:

- intergrated Python 2 and 3 sources, running on Python 2.6, 2.7, 3.3 and 3.4.
- round trip mode that **includes comments** (block mode, key ordering kept)
- support for simple lists as mapping keys by transformatopm to tuples
- omap generates ordereddict (C) on Python 2, collections.OrderedDict
  on Python 3.
- some YAML 1.2 enhancements (``0o`` octal prefix, ``\/`` escape)
- pep8 compliance
- tox and py.test based testing


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
<http://www.voidspace.org.uk/python/configobj.html>` library by Foord
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

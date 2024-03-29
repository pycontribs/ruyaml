********
Overview
********

``ruyaml`` is a YAML 1.2 loader/dumper package for Python. It is a
derivative of Kirill Simonov's `PyYAML 3.11
<https://bitbucket.org/xi/pyyaml>`_.

``ruyaml`` supports `YAML 1.2`_ and has round-trip loaders and dumpers.

- comments
- block style and key ordering are kept, so you can diff the round-tripped
  source
- flow style sequences ( 'a: b, c, d') (based on request and test by
  Anthony Sottile)
- anchor names that are hand-crafted (i.e. not of the form``idNNN``)
- `merges <http://yaml.org/type/merge.html>`_ in dictionaries are preserved

This preservation is normally not broken unless you severely alter
the structure of a component (delete a key in a dict, remove list entries).
Reassigning values or replacing list items, etc., is fine.

For the specific 1.2 differences see :ref:`yaml-1-2-support`

Although individual indentation of lines is not preserved, you can specify
separate indentation levels for mappings and sequences (counting for sequences
does **not** include the dash for a sequence element) and specific offset of
block sequence dashes within that indentation.


Although ``ruyaml`` still allows most of the PyYAML way of doing
things, adding features required a different API then the transient
nature of PyYAML's ``Loader`` and ``Dumper``. Starting with
``ruyaml`` version 0.15.0 this new API gets introduced. Old ways
that get in the way will be removed, after first generating warnings
on use, then generating an error. In general a warning in version 0.N.x will become an
error in 0.N+1.0


Many of the bugs filed against PyYAML, but that were never
acted upon, have been fixed in ``ruyaml``

.. _tox: https://pypi.python.org/pypi/tox
.. _py.test: http://pytest.org/latest/
.. _YAML 1.1: http://www.yaml.org/spec/1.1/spec.html
.. _YAML 1.2: http://www.yaml.org/spec/1.2/spec.html
.. _PyPI: https://pypi.python.org/pypi
.. _ruyaml: https://pypi.python.org/pypi/ruyaml

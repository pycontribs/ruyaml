***********************
Differences with PyYAML
***********************

.. parsed-literal::

    *If I have seen further, it is by standing on the shoulders of giants*.
                                                    Isaac Newton (1676)



``ruyaml`` is a derivative of Kirill Simonov's `PyYAML 3.11
<https://bitbucket.org/xi/pyyaml>`_ and would not exist without that
excellent base to start from.

The following a summary of the major differences with PyYAML 3.11

.. _yaml-1-2-support:

Defaulting to YAML 1.2 support
++++++++++++++++++++++++++++++

PyYAML supports the `YAML 1.1`_ standard, ``ruyaml`` supports
`YAML 1.2`_ as released in 2009.

- YAML 1.2 dropped support for several features unquoted ``Yes``,
  ``No``, ``On``, ``Off``
- YAML 1.2 no longer accepts strings that start with a ``0`` and solely
  consist of number characters as octal, you need to specify such strings with
  ``0o[0-7]+`` (zero + lower-case o for octal + one or more octal characters).
- YAML 1.2 no longer supports `sexagesimals
  <https://en.wikipedia.org/wiki/Sexagesimal>`_, so the string scalar
  ``12:34:56`` doesn't need quoting.
- ``\/`` escape for JSON compatibility
- correct parsing of floating point scalars with exponentials

unless the YAML document is loaded with an explicit ``version==1.1`` or
the document starts with::

    % YAML 1.1

, ``ruyaml`` will load the document as version 1.2.


Python Compatibility
++++++++++++++++++++

``ruyaml`` requires Python 3.7 or later.

Fixes
+++++

- ``ruyaml`` follows the ``indent`` keyword argument on scalars
  when dumping.
- ``ruyaml`` allows ``:`` in plain scalars, as long as these are not
  followed by a space (as per the specification)


Testing
+++++++

``ruyaml`` is tested using `tox`_ and `py.test`_. In addition to
new tests, the original PyYAML
test framework is called from within ``tox`` runs.

Before versions are pushed to PyPI, ``tox`` is invoked, and has to pass, on all
supported Python versions, on PyPI as well as flake8/pep8

API
+++

Starting with 0.15 the API for using ``ruyaml`` has diverged allowing
easier addition of new features.

.. _tox: https://pypi.python.org/pypi/tox
.. _py.test: http://pytest.org/latest/
.. _YAML 1.1: http://www.yaml.org/spec/1.1/spec.html
.. _YAML 1.2: http://www.yaml.org/spec/1.2/spec.html
.. _PyPI: https://pypi.python.org/pypi
.. _ruyaml: https://pypi.python.org/pypi/ruyaml

**********
Installing
**********

Make sure you have a recent version of ``pip`` and ``setuptools``
installed. The later needs environment marker support
(``setuptools>=20.6.8``) and that is e.g.  bundled with Python 3.4.6 but
not with 3.4.4. It is probably best to do::

    pip install -U pip setuptools wheel

in your environment (``virtualenv``, (Docker) container, etc) before
installing ``ruyaml``.

``ruyaml`` itself should be installed from PyPI_ using::

    pip install ruyaml

If you want to process jinja2/YAML templates (which are not valid YAML
with the default jinja2 markers), do ``pip install
ruyaml[jinja2]`` (you might need to quote the last argument
because of the ``[]``)


There also is a commandline utility ``yaml`` available after installing::

    pip install ruyaml.cmd

that allows for round-trip testing/re-indenting and conversion of YAML
files (JSON,INI,HTML tables)

Optional requirements
+++++++++++++++++++++

If you have the the header files for your Python executables installed
then you can use the (non-roundtrip), but faster, C loader and emitter.

On Debian systems you should use::

    sudo apt-get install python3-dev

you can leave out ``python3-dev`` if you don't use python3

For CentOS (7) based systems you should do::

    sudo yum install python-devel

.. _tox: https://pypi.python.org/pypi/tox
.. _py.test: http://pytest.org/latest/
.. _YAML 1.1: http://www.yaml.org/spec/1.1/spec.html
.. _YAML 1.2: http://www.yaml.org/spec/1.2/spec.html
.. _PyPI: https://pypi.python.org/pypi
.. _ruyaml: https://pypi.python.org/pypi/ruyaml

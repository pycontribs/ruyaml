************
Contributing
************

All contributions to ``ruyaml`` are welcome.
Please post an issue or, if possible, a pull request (PR) on github.

Please don't use issues to post support questions.

TODO:: The maintainers of ruyaml don't have an official support channel yet.

Documentation
=============

The documentation for ``ruyaml`` is written in the `ReStructured Text
<http://docutils.sourceforge.net/rst.html>`_ format and follows the `Sphinx
Document Generator <https://www.sphinx-doc.org/>`_'s conventions.

Code
====

Code changes are welcome as well, but anything beyond a minor change should be
tested (``tox``/``pytest``), checked for typing conformance (``mypy``) and pass
pep8 conformance (``flake8``).

In my experience it is best to use two ``virtualenv`` environments, one with the
latest Python from the 2.7 series, the other with 3.5 or 3.6. In the
site-packages directory of each virtualenv make a soft link to the ruyaml
directory of your (cloned and checked out) copy of the repository. Do not under
any circumstances run ``pip install -e .`` it will
not work (at least not until these commands are fixed to support packages with
namespaces).

You can install ``tox``, ``pytest``, ``mypy`` and ``flake8`` in the Python3
``virtualenv``, or in a ``virtualenv``  of their own. If all of these commands
pass without warning/error, you can create your pull-request.

Flake
+++++

The `Flake8 <https://flake8.pycqa.org>`_ configuration is part of ``setup.cfg``::

    [flake8]
    show-source = True
    max-line-length = 95
    ignore = F405

The suppress of F405 is necessary to allow ``from xxx import *``.

Please make sure your checked out source passes ``flake8`` without test (it should).
Then make your changes pass without any warnings/errors.

Tox/pytest
++++++++++

Whether you add something or fix some bug with your code changes, first add one
or more tests that fail in the unmodified source when running ``tox``. Once that
is in place add your code, which should have as a result that your added test(s)
no longer fail, and neither should any other existing tests.

Typing/mypy
+++++++++++

You should run ``mypy`` from ``ruyaml``'s source directory::

    mypy --strict --follow-imports silent lib/ruyaml/*.py

This command should give no errors or warnings.


Vulnerabilities
===============

If you find a vulnerability in ``ruyaml`` (e.g. that would show the ``safe``
and ``rt`` loader are not safe due to a bug in the software)), please contact
the maintainers directly via email.

After the vulnerability is removed, and affected parties notified to allow them
to update versions, the vulnerability will be published, and your role in
finding/resolving this properly attributed.

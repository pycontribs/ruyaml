ruyaml
======

``ruyaml`` package is a fork of ``ruamel.yaml`` aimed to made in order to
secure the future of the library, mainly by having a pool of maintainers.

Notes
=====

- The current version has the same API as the "ruamel.yaml" package.
  However, it will install the `ruyaml` python module. Thus, simply
  replace ``from ruamel import yaml`` with ``import ruyaml as yaml``
  (or equivalent) and you're all set.
- python3.6 is the minimal version of python supported


:version:       0.17.4
:updated:       2021-04-07
:documentation: http://ruyaml.readthedocs.io
:repository:    https://github.com/pycontribs/ruyaml.git
:pypi:          https://pypi.org/project/ruyaml/

*The 0.16.13 release was the last that will tested to be working on Python 2.7.
The 0.17 series will still be tested on Python 3.5, but the 0.18 will not. The
0.17 series will also stop support for the old PyYAML functions, so a `YAML()` instance
will need to be created.*

*The 0.17 series will also see changes in how comments are attached during
roundtrip. This will result in backwards incompatibilities on the `.ca` data and
it might even be necessary for documented methods that handle comments.*

*Please adjust your dependencies accordingly if necessary. (`ruamel.yaml<0.17`)*


Starting with version 0.15.0 the way YAML files are loaded and dumped
is changing. See the API doc for details.  Currently existing
functionality will throw a warning before being changed/removed.
**For production systems you should pin the version being used with
``ruamel.yaml<=0.15``**. There might be bug fixes in the 0.14 series,
but new functionality is likely only to be available via the new API.

If your package uses ``ruamel.yaml`` and is not listed on PyPI, drop
me an email, preferably with some information on how you use the
package (or a link to the repository) and I'll keep you informed
when the status of the API is stable enough to make the transition.

* `Overview <http://yaml.readthedocs.org/en/latest/overview.html>`_
* `Installing <http://yaml.readthedocs.org/en/latest/install.html>`_
* `Basic Usage <http://yaml.readthedocs.org/en/latest/basicuse.html>`_
* `Details <http://yaml.readthedocs.org/en/latest/detail.html>`_
* `Examples <http://yaml.readthedocs.org/en/latest/example.html>`_
* `API <http://yaml.readthedocs.org/en/latest/api.html>`_
* `Differences with PyYAML <http://yaml.readthedocs.org/en/latest/pyyaml.html>`_

.. image:: https://readthedocs.org/projects/yaml/badge/?version=stable
   :target: https://yaml.readthedocs.org/en/stable

.. image:: https://bestpractices.coreinfrastructure.org/projects/1128/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/1128

.. image:: https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/ruamel.yaml/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://pypi.org/project/oitnb/

.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
   :target: http://mypy-lang.org/

ChangeLog
=========

.. should insert NEXT: at the beginning of line for next key (with empty line)

0.17.4 (2021-04-07):
  - prevent (empty) comments from throwing assertion error (issue 351
    reported by  `William Kimball <https://sourceforge.net/u/william303/>`__)
    comments (or empty line) will be dropped

0.17.3 (2021-04-07):
  - fix for issue 382 caused by an error in a format string (reported by
    `William Kimball <https://sourceforge.net/u/william303/>`__)
  - allow expansion of aliases by setting ``yaml.composer.return_alias = lambda s: copy.deepcopy(s)``
     (as per `Stackoverflow answer <https://stackoverflow.com/a/66983530/1307905>`__)

0.17.2 (2021-03-29):
  - change -py2.py3-none-any.whl to -py3-none-any.whl, and remove 0.17.1

0.17.1 (2021-03-29):
   - added 'Programming Language :: Python :: 3 :: Only', and removing
     0.17.0 from PyPI (reported by `Alasdair Nicol <https://sourceforge.net/u/alasdairnicol/>`__)

0.17.0 (2021-03-26):
  - removed because of incomplete classifiers
  - this release no longer supports Python 2.7, most if not all Python 2
    specific code is removed. The 0.17.x series is the last to  support Python 3.5
    (this also allowed for removal of the dependency  on ``ruamel.std.pathlib``)
  - remove Python2 specific code branches and adaptations (u-strings)
  - prepare % code for f-strings using ``_F``
  - allow PyOxidisation (`issue 324 <https://sourceforge.net/p/ruamel-yaml/tickets/324/>`__
    resp. `issue 171 <https://github.com/indygreg/PyOxidizer/issues/171>`__)
  - replaced Python 2 compatible enforcement of keyword arguments with '*'
  - the old top level *functions* ``load``, ``safe_load``, ``round_trip_load``,
    ``dump``, ``safe_dump``, ``round_trip_dump``, ``scan``, ``parse``,
    ``compose``, ``emit``, ``serialize`` as well as their ``_all`` variants for
    multi-document streams, now issue a ``PendingDeprecationning`` (e.g. when run
    from pytest, but also Python is started with ``-Wd``). Use the methods on
    ``YAML()``, which have been extended.
  - fix for issue 376: indentation changes could put literal/folded scalar to start
    before the ``#`` column of a following comment. Effectively making the comment
    part of the scalar in the output. (reported by
    `Bence Nagy <https://sourceforge.net/u/underyx/>`__)


0.16.13 (2021-03-05):
  - fix for issue 359: could not update() CommentedMap with keyword arguments
    (reported by `Steve Franchak <https://sourceforge.net/u/binaryadder/>`__)
  - fix for issue 365: unable to dump mutated TimeStamp objects
    (reported by Anton Akmerov <https://sourceforge.net/u/akhmerov/>`__)
  - fix for issue 371: unable to addd comment without starting space
    (reported by 'Mark Grandi <https://sourceforge.net/u/mgrandi>`__)
  - fix for issue 373: recursive call to walk_tree not preserving all params
    (reported by `eulores <https://sourceforge.net/u/eulores/>`__)
  - a None value in a flow-style sequence is now dumped as `null` instead
    of `!!null ''` (reported by mcarans on
    `StackOverlow <https://stackoverflow.com/a/66489600/1307905>`__)

0.16.12 (2020-09-04):
  - update links in doc

0.16.11 (2020-09-03):
  - workaround issue with setuptools 0.50 and importing pip ( fix by jaraco
    https://github.com/pypa/setuptools/issues/2355#issuecomment-685159580 )

0.16.10 (2020-02-12):
  - (auto) updated image references in README to sourceforge

0.16.9 (2020-02-11):
  - update CHANGES

0.16.8 (2020-02-11):
  - update requirements so that ruamel.yaml.clib is installed for 3.8,
    as it has become available (via manylinux builds)

0.16.7 (2020-01-30):
  - fix typchecking issue on TaggedScalar (reported by Jens Nielsen)
  - fix error in dumping literal scalar in sequence with comments before element
    (reported by `EJ Etherington <https://sourceforge.net/u/ejether/>`__)

0.16.6 (2020-01-20):
  - fix empty string mapping key roundtripping with preservation of quotes as `? ''`
    (reported via email by Tomer Aharoni).
  - fix incorrect state setting in class constructor (reported by `Douglas Raillard
    <https://bitbucket.org/%7Bcf052d92-a278-4339-9aa8-de41923bb556%7D/>`__)
  - adjust deprecation warning test for Hashable, as that no longer warns (reported
    by `Jason Montleon <https://bitbucket.org/%7B8f377d12-8d5b-4069-a662-00a2674fee4e%7D/>`__)

0.16.5 (2019-08-18):
  - allow for ``YAML(typ=['unsafe', 'pytypes'])``

0.16.4 (2019-08-16):
  - fix output of TAG directives with # (reported by `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)


0.16.3 (2019-08-15):
  - split construct_object
  - change stuff back to keep mypy happy
  - move setting of version based on YAML directive to scanner, allowing to
    check for file version during TAG directive scanning

0.16.2 (2019-08-15):
  - preserve YAML and TAG directives on roundtrip, correctly output #
    in URL for YAML 1.2 (both reported by `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)

0.16.1 (2019-08-08):
  - Force the use of new version of ruamel.yaml.clib (reported by `Alex Joz
    <https://bitbucket.org/%7B9af55900-2534-4212-976c-61339b6ffe14%7D/>`__)
  - Allow '#' in tag URI as these are allowed in YAML 1.2 (reported by
    `Thomas Smith
    <https://bitbucket.org/%7Bd4c57a72-f041-4843-8217-b4d48b6ece2f%7D/>`__)

0.16.0 (2019-07-25):
  - split of C source that generates .so file to ruamel.yaml.clib
  - duplicate keys are now an error when working with the old API as well


----

For older changes see the file
`CHANGES <https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree/CHANGES>`_

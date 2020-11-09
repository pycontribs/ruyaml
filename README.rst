ruyaml
======

``ruyaml`` package is a fork of ``ruamel.yaml`` aimed to made in order to
secure the future of the library, mainly by having a pool of maintainers.

Notes
=====

- The current version has the same API as the "ruamel.yaml" package.
  However, it will install the `ruyaml` python module. Thus, simply
  replace ``from yuamel import yaml`` with ``import ruyaml as yaml``
  (or equivalent) and you're all set.
- python3.6 is the minimal version of python supported

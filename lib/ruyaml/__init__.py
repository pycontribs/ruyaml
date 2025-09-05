# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

if False:  # MYPY
    from typing import Any, Dict  # NOQA

_package_data = dict(
    full_package_name='ruyaml',
    version_info=(0, 18, 15),
    __version__='0.18.15',
    author='ruyaml contributors',
    author_email='none.yet@github.org',
    description='ruyaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order',  # NOQA
    entry_points=None,
    since=2014,
    extras_require={
        ':platform_python_implementation=="CPython" and python_version<"3.8"': [
            'ruyaml.clib>=0.1.2',
        ],
    },
)  # type: Dict[Any, Any]


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

try:
    from .cyaml import *  # NOQA

    __with_libyaml__ = True
except (ImportError, ValueError):  # for Jython
    __with_libyaml__ = False

from ruyaml.main import *  # NOQA

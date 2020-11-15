# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

if False:  # MYPY
    from typing import Any, Dict  # NOQA

_package_data = dict(
    full_package_name='ruyaml',
    version_info=(0, 16, 7),
    __version__='0.16.7',
    author='ruyaml contributors',
    author_email='none.yet@github.org',
    description='ruyaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order',  # NOQA
    entry_points=None,
    since=2014,
    extras_require={
        ':platform_python_implementation=="CPython" and python_version<="2.7"': [
            'ruamel.ordereddict',
        ],
        ':platform_python_implementation=="CPython" and python_version<"3.8"': [
            'ruyaml.clib>=0.1.2',
        ],
        'jinja2': ['ruyaml.jinja2>=0.2'],
        'docs': ['ryd'],
    },
    # NOQA
    # test='#include "ext/yaml.h"\n\nint main(int argc, char* argv[])\n{\nyaml_parser_t parser;\nparser = parser;  /* prevent warning */\nreturn 0;\n}\n',  # NOQA
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
        'Typing :: Typed',
    ],
    keywords='yaml 1.2 parser round-trip preserve quotes order config',
    read_the_docs='yaml',
    supported=[(2, 7), (3, 5)],  # minimum
    tox=dict(
        env='*pn',  # also test narrow Python 2.7.15 for unicode patterns
        fl8excl='_test/lib',
    ),
    universal=True,
    rtfd='yaml',
)  # type: Dict[Any, Any]


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

try:
    from .cyaml import *  # NOQA

    __with_libyaml__ = True
except (ImportError, ValueError):  # for Jython
    __with_libyaml__ = False

from ruyaml.main import *  # NOQA

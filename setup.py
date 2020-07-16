from setuptools import setup, find_packages

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name='ruyaml',
    use_scm_version={"version_scheme": "guess-next-dev", "local_scheme": "dirty-tag"},
    setup_requires=["setuptools_scm"],
    author='Matthias Urlichs',
    author_email='matthias@urlichs.de',
    description='ruyaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order',  # NOQA
    entry_points=None,
    since=2014,
    extras_require={':platform_python_implementation=="CPython" and python_version<"3.9"': [
            'ruyaml.clib>=0.1.2',
        ], 'jinja2': ['ruyaml.jinja2>=0.2'], 'docs': ['ryd']},
    # NOQA
    # test='#include "ext/yaml.h"\n\nint main(int argc, char* argv[])\n{\nyaml_parser_t parser;\nparser = parser;  /* prevent warning */\nreturn 0;\n}\n',  # NOQA
    classifiers=[
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
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
        env='*',  # remove 'pn', no longer test narrow Python 2.7 for unicode patterns and PyPy
        deps='pathlib',
        fl8excl='_test/lib',
    ),
    universal=True,
    rtfd='ruyaml',
)

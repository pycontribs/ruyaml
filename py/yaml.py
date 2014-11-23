# coding: utf-8

"""
this is the source for the yaml utility
"""

from __future__ import print_function

import sys
import os
import io

from ruamel.std.argparse import ProgramBase, option, sub_parser, version, \
    CountAction, SmartFormatter
# from ruamel.appconfig import AppConfig
from . import __version__

import ruamel.yaml


class YAML:
    def __init__(self, args, config):
        self._args = args
        self._config = config

    def from_json(self):
        # use roundtrip to preserver order
        errors = 0
        docs = []
        for file_name in self._args.file:
            inp = open(file_name).read()
            loader = ruamel.yaml.RoundTripLoader
            docs.append(ruamel.yaml.load(inp, loader))
        stream = io.StringIO()
        dumper = ruamel.yaml.RoundTripDumper
        print(ruamel.yaml.dump_all(docs, Dumper=dumper))
        return 1 if errors else 0

    def round_trip(self):
        errors = 0
        warnings = 0
        for file_name in self._args.file:
            inp = open(file_name).read()
            outp = self.round_trip_single(inp)
            if inp == outp:
                if self._args.verbose > 0:
                    print(u"{0}: ok".format(file_name))
                continue
            warnings += 1
            stabelize = []
            if inp.split() != outp.split():
                errors += 1
                stabelize.append(u"drops info on round trip")
            else:
                if self.round_trip_single(outp) == outp:
                    stabelize.append(u"stabelizes on second round trip")
                else:
                    errors += 1
            ncoutp = self.round_trip_single(inp, drop_comment=True)
            if self.round_trip_single(ncoutp, drop_comment=True) == ncoutp:
                stabelize.append(u"ok without comments")
            print("{0}:\n     {1}".format(file_name, u', '.join(stabelize)))
            self.diff(inp, outp, file_name)
        return 2 if errors > 0 else 1 if warnings > 0 else 0

    def round_trip_single(self, inp, drop_comment=False):
        loader = ruamel.yaml.SafeLoader if drop_comment else \
            ruamel.yaml.RoundTripLoader
        code = ruamel.yaml.load(inp, loader)
        stream = io.StringIO()
        dumper = ruamel.yaml.SafeDumper if drop_comment else \
            ruamel.yaml.RoundTripDumper
        return ruamel.yaml.dump(code, Dumper=dumper)

    def diff(self, inp, outp, file_name):
        import difflib
        inl = inp.splitlines(True)  # True for keepends
        outl = outp.splitlines(True)
        diff = difflib.unified_diff(inl, outl, file_name, 'round trip YAML')
        sys.stdout.writelines(diff)


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


class YAML_Cmd(ProgramBase):
    def __init__(self):
        super(YAML_Cmd, self).__init__(
            formatter_class=SmartFormatter,
            aliases=True,
        )
        self._config = None

    # you can put these on __init__, but subclassing YAML_Cmd
    # will cause that to break
    @option('--verbose', '-v',
            help='increase verbosity level', action=CountAction,
            const=1, nargs=0, default=0, global_option=True)
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        yaml = YAML(self._args, self._config)
        if self._args.func:
            return self._args.func(yaml)

    def parse_args(self):
        # self._config = AppConfig(
        #     'yaml',
        #     filename=AppConfig.check,
        #     parser=self._parser,  # sets --config option
        #     warning=to_stdout,
        #     add_save=False,  # add a --save-defaults (to config) option
        # )
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        # self._config.set_defaults()
        self._parse_args()

    @sub_parser(
        aliases=['round-trip'],
        help='test round trip on YAML data',
        description='test round trip on YAML data',
    )
    @option('file', nargs='+')
    def rt(self, yaml):
        return yaml.round_trip()

    @sub_parser(
        aliases=['from-json'],
        help='convert json to block YAML',
        description='convert json to block YAML',
    )
    @option('file', nargs='+')
    def json(self, yaml):
        return yaml.from_json()


def main():
    n = YAML_Cmd()
    n.parse_args()
    sys.exit(n.run())

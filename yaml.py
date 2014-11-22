# coding: utf-8

from __future__ import print_function

import sys
import os

from ruamel.std.argparse import ProgramBase, option, sub_parser, version, \
    CountAction, SmartFormatter
from ruamel.appconfig import AppConfig
from . import __version__


class YAML:
    def __init__(self, args, config):
        self._args = args
        self._config = config


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


class YAML_Cmd(ProgramBase):
    def __init__(self):
        super(YAML_Cmd, self).__init__(
            formatter_class=SmartFormatter
        )

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
        # if self._args.func:
        #     return self._args.func()

    def parse_args(self):
        #self._config = AppConfig(
        #    'yaml',
        #    filename=AppConfig.check,
        #    parser=self._parser,  # sets --config option
        #    warning=to_stdout,
        #    add_save=False,  # add a --save-defaults (to config) option
        #)
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        #self._config.set_defaults()
        self._parse_args()

    # @sub_parser(help='some command specific help for tmux')
    # @option('--session-name', default='abc')
    # def tmux(self):
    #     from plumbum.cmd import tmux
    #     from plumbum.commands.processes import ProcessExecutionError


def main():
    n = YAML_Cmd()
    n.parse_args()
    n.run()

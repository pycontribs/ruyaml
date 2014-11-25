# coding: utf-8

"""
this is the source for the yaml utility
"""

from __future__ import print_function

import sys
import os
import io
from textwrap import dedent

from ruamel.std.argparse import ProgramBase, option, sub_parser, version, \
    CountAction, SmartFormatter
# from ruamel.appconfig import AppConfig
from . import __version__

import ruamel.yaml
from ruamel.yaml.compat import ordereddict, DBG_TOKEN, DBG_EVENT, DBG_NODE


class YAML:
    def __init__(self, args, config):
        self._args = args
        self._config = config

    def from_ini(self):
        from configobj import ConfigObj
        errors = 0
        doc = []
        cfg = ConfigObj(open(self._args.file))
        # print(cfg)
        for line in self.walk_configobj(cfg):
            if not line.strip():
                continue
            # print(line)
            doc.append(line)
        # print('--------------')
        joined = '\n'.join(doc)
        rto = self.round_trip_single(joined)
        print(rto, end='')  # already has eol at eof
        # print()
        # if rto != joined:
        #     self.diff(joined, rto, "test.ini")
        return 1 if errors else 0

    def test(self):
        self._args.event = self._args.node = True
        dbg = 0
        if self._args.event:
            dbg |= DBG_EVENT
        if self._args.node:
            dbg |= DBG_NODE
        os.environ['YAMLDEBUG'] = str(dbg)
        if False:
            x = ruamel.yaml.comment.Comment()
            print(sys.getsizeof(x))
            return

        def print_input(input):
            print(input, end='')
            print('-' * 15)

        def print_tokens(input):
            print('Tokens ' + '#' * 60)
            tokens = ruamel.yaml.scan(input, ruamel.yaml.RoundTripLoader)
            for idx, token in enumerate(tokens):
                # print(token.start_mark)
                # print(token.end_mark)
                print("{0:2} {1}".format(idx, token))

        def rt_events(input):
            dumper = ruamel.yaml.RoundTripDumper
            events = ruamel.yaml.parse(input, ruamel.yaml.RoundTripLoader)
            print(ruamel.yaml.emit(events, indent=False, Dumper=dumper))

        def rt_nodes(input):
            dumper = ruamel.yaml.RoundTripDumper
            nodes = ruamel.yaml.compose(input, ruamel.yaml.RoundTripLoader)
            print(ruamel.yaml.serialize(nodes, indent=False, Dumper=dumper))

        def print_events(input):
            print('Events ' + '#' * 60)
            events = ruamel.yaml.parse(input, ruamel.yaml.RoundTripLoader)
            for idx, event in enumerate(events):
                print("{0:2} {1}".format(idx, event))

        def print_nodes(input):
            print('Nodes ' + '#' * 60)
            x = ruamel.yaml.compose(input, ruamel.yaml.RoundTripLoader)
            x.dump()  # dump the node

        input = dedent("""
        application: web2py
        version: 1
        runtime: python27
        api_version: 1
        threadsafe: false

        default_expiration: "24h"

        handlers:
        - url: /(?P<a>.+?)/static/(?P<b>.+)
          static_files: 'applications/\\1/static/\\2'
          upload: applications/(.+?)/static/(.+)
          secure: optional
        """)

        print_input(input)
        print_tokens(input)
        print_events(input)
        # rt_events(input)
        print_nodes(input)
        # rt_nodes(input)

        data = ruamel.yaml.load(input, ruamel.yaml.RoundTripLoader)
        print('data', data)
        if False:
            data['american'][0] = 'Fijenoord'
            l = data['american']
        l = data
        if True:
            # print type(l), '\n', dir(l)
            comment = getattr(l, '_yaml_comment', None)
            print('comment_1', comment)
        dumper = ruamel.yaml.RoundTripDumper
        print('>>>>>>>>>>')
        # print(ruamel.yaml.dump(data, default_flow_style=False,
        #    Dumper=dumper), '===========')
        print("{0}=========".format(ruamel.yaml.dump(data, Dumper=dumper)))
        comment = getattr(l, '_yaml_comment', None)
        print('comment_2', comment)

        # test end

    @staticmethod
    def walk_configobj(cfg):
        from configobj import ConfigObj
        assert isinstance(cfg, ConfigObj)
        for c in cfg.initial_comment:
            yield c
        for s in YAML.walk_section(cfg):
            yield s
        for c in cfg.final_comment:
            yield c

    @staticmethod
    def walk_section(s, level=0):
        from configobj import Section
        assert isinstance(s, Section)
        indent = '  ' * level
        for name in s.scalars:
            for c in s.comments[name]:
                yield indent + c.strip()
            line = '{0}{1}: {2}'.format(indent, name, s[name])
            c = s.inline_comments[name]
            if c:
                line += ' ' + c
            yield line
        for name in s.sections:
            for c in s.comments[name]:
                yield indent + c.strip()
            line = '{0}{1}:'.format(indent, name)
            c = s.inline_comments[name]
            if c:
                line += ' ' + c
            yield line
            for val in YAML.walk_section(s[name], level=level+1):
                yield val

    def from_json(self):
        # use roundtrip to preserver order
        errors = 0
        docs = []
        for file_name in self._args.file:
            inp = open(file_name).read()
            loader = ruamel.yaml.RoundTripLoader
            docs.append(ruamel.yaml.load(inp, loader))
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
        dumper = ruamel.yaml.SafeDumper if drop_comment else \
            ruamel.yaml.RoundTripDumper
        return ruamel.yaml.dump(code, Dumper=dumper)

    def diff(self, inp, outp, file_name):
        import difflib
        inl = inp.splitlines(True)  # True for keepends
        outl = outp.splitlines(True)
        diff = difflib.unified_diff(inl, outl, file_name, 'round trip YAML')
        # 2.6 difflib has trailing space on filename lines %-)
        strip_trailing_space = sys.version_info < (2, 7)
        for line in diff:
            if strip_trailing_space and line[:4] in ['--- ', '+++ ']:
                line = line.rstrip() + '\n'
            sys.stdout.write(line)


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

    @sub_parser(
        aliases=['from-ini'],
        help='convert .ini/config to block YAML',
        description='convert .ini/config to block YAML',
    )
    @option('file')
    def ini(self, yaml):
        return yaml.from_ini()

    if 'test' in sys.argv:
        @sub_parser(
            description='internal test function',
        )
        @option('file', nargs='*')
        def test(self, yaml):
            return yaml.test()


def main():
    n = YAML_Cmd()
    n.parse_args()
    sys.exit(n.run())

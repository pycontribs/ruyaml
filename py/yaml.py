# coding: utf-8

"""
this is the source for the yaml utility
"""

from __future__ import print_function
from __future__ import absolute_import


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
from ruamel.yaml.configobjwalker import configobj_walker


def yaml_to_html2(code):
    buf = io.StringIO()
    buf.write(u'<HTML>\n')
    buf.write(u'<HEAD>\n')
    buf.write(u'</HEAD>\n')
    buf.write(u'<BODY>\n')
    buf.write(u'<TABLE>\n')
    if isinstance(code, dict):
        for k in code:
            buf.write(u'  <TR>\n')
            for x in [k] + code[k]:
                buf.write(u'    <TD>{0}</TD>\n'.format(x))
            buf.write(u'  </TR>\n')
    buf.write(u'<TABLE>\n')
    buf.write(u'</BODY>\n')
    buf.write(u'</HTML>\n')
    return buf.getvalue()


def yaml_to_html(code, level):
    if level == 2:
        return yaml_to_html2(code)
    elif level == 3:
        return yaml_to_html3(code)
    raise NotImplementedError


class YAML:
    def __init__(self, args, config):
        self._args = args
        self._config = config

    def from_ini(self):
        try:
            from configobj import ConfigObj
        except ImportError:
            print("to convert from .ini you need to install configobj:")
            print("  pip install configobj:")
            sys.exit(1)
        errors = 0
        doc = []
        cfg = ConfigObj(open(self._args.file))
        for line in configobj_walker(cfg):
            doc.append(line)
        joined = '\n'.join(doc)
        rto = self.round_trip_single(joined)
        if self._args.basename:
            out_fn = os.path.splitext(self._args.file)[0] + '.yaml'
            if self._args.verbose > 0:
                print('writing', out_fn)
            with open(out_fn, 'w') as fp:
                print(rto, end='', file=fp)  # already has eol at eof
        else:
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
            print('Tokens (from scanner) ' + '#' * 50)
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
            print('Events (from parser) ' + '#' * 50)
            events = ruamel.yaml.parse(input, ruamel.yaml.RoundTripLoader)
            for idx, event in enumerate(events):
                print("{0:2} {1}".format(idx, event))

        def print_nodes(input):
            print('Nodes (from composer) ' + '#' * 50)
            x = ruamel.yaml.compose(input, ruamel.yaml.RoundTripLoader)
            x.dump()  # dump the node

        def scan_file(file_name):
            inp = open(file_name).read()
            print('---------\n', file_name)
            print('---', repr(self.first_non_empty_line(inp)))
            print('<<<', repr(self.last_non_empty_line(inp)))

        if True:
            for x in self._args.file:
                scan_file(x)
            return

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

        input = dedent("""\
        a:
            b: foo
            c: bar
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
        print("{0}=========".format(ruamel.yaml.dump(
            data,
            indent=4,
            Dumper=dumper)))
        comment = getattr(l, '_yaml_comment', None)
        print('comment_2', comment)

        # test end

    def from_json(self):
        # use roundtrip to preserver order
        errors = 0
        docs = []
        for file_name in self._args.file:
            inp = open(file_name).read()
            loader = ruamel.yaml.Loader # RoundTripLoader
            docs.append(ruamel.yaml.load(inp, loader))
        dumper = ruamel.yaml.RoundTripDumper
        print(ruamel.yaml.dump_all(
            docs, Dumper=dumper,
            default_flow_style=self._args.flow))
        return 1 if errors else 0

    def to_htmltable(self):
        def vals(x):
            if isinstance(x, list):
                return x
            if isinstance(x, (dict, ordereddict)):
                return x.values()
            return []

        def seek_levels(x, count=0):
            my_level = count
            sub_level = 0
            for v in vals(x):
                if v is None:
                    continue
                sub_level = max(sub_level, seek_levels(v, my_level+1))
            return max(my_level, sub_level)

        inp = open(self._args.file).read()
        loader = ruamel.yaml.RoundTripLoader
        code = ruamel.yaml.load(inp, loader)
        # assert isinstance(code, [ruamel.yaml.comments.CommentedMap])
        assert isinstance(code, (dict, list))
        levels = seek_levels(code)
        if self._args.level:
            print("levels:", levels)
            return
        print(yaml_to_html(code, levels))

    def from_html(self):
        from .convert.html import HTML2YAML
        h2y = HTML2YAML(self._args)
        with open(self._args.file) as fp:
            print(h2y(fp.read()))

    def from_csv(self):
        from .convert.from_csv import CSV2YAML
        c2y = CSV2YAML(self._args)
        c2y(self._args.file)

    def round_trip(self):
        errors = 0
        warnings = 0
        for file_name in self._args.file:
            inp = open(file_name).read()
            e, w, stabilize, outp = self.round_trip_input(inp)
            if w == 0:
                if self._args.verbose > 0:
                    print(u"{0}: ok".format(file_name))
                continue
            if self._args.save:
                backup_file_name = file_name + '.orig'
                if not os.path.exists(backup_file_name):
                    os.rename(file_name, backup_file_name)
                with open(file_name, 'w') as ofp:
                    ofp.write(outp)
            if not self._args.save or self._args.verbose > 0:
                print("{0}:\n     {1}".format(file_name, u', '.join(stabilize)))
                self.diff(inp, outp, file_name)
            errors += e
            warnings += w
        if errors > 0:
            return 2
        if warnings > 0:
            return 1
        return 0

    def round_trip_input(self, inp):
        errors = 0
        warnings = 0
        stabilize = []
        outp = self.round_trip_single(inp)
        if inp == outp:
            return errors, warnings, stabilize, outp
        warnings += 1
        if inp.split() != outp.split():
            errors += 1
            stabilize.append(u"drops info on round trip")
        else:
            if self.round_trip_single(outp) == outp:
                stabilize.append(u"stabilizes on second round trip")
            else:
                errors += 1
        ncoutp = self.round_trip_single(inp, drop_comment=True)
        if self.round_trip_single(ncoutp, drop_comment=True) == ncoutp:
            stabilize.append(u"ok without comments")
        return errors, warnings, stabilize, outp

    def round_trip_single(self, inp, drop_comment=False):
        explicit_start=self.first_non_empty_line(inp) == '---'
        explicit_end=self.last_non_empty_line(inp) == '...'
        indent = self._args.indent
        loader = ruamel.yaml.SafeLoader if drop_comment else \
            ruamel.yaml.RoundTripLoader
        code = ruamel.yaml.load(inp, loader)
        dumper = ruamel.yaml.SafeDumper if drop_comment else \
            ruamel.yaml.RoundTripDumper
        return ruamel.yaml.dump(
            code,
            Dumper=dumper,
            indent=indent,
            explicit_start=explicit_start,
            explicit_end=explicit_end,
        )

    def first_non_empty_line(self, txt):
        """return the first non-empty line of a block of text (stripped)
        do not split or strip the complete txt
        """
        pos = txt.find('\n')
        prev_pos = 0
        while pos >= 0:
            segment = txt[prev_pos:pos].strip()
            if segment:
                break
            # print (pos, repr(segment))
            prev_pos = pos
            pos = txt.find('\n', pos+1)
        return segment

    def last_non_empty_line(self, txt):
        """return the last non-empty line of a block of text (stripped)
        do not split or strip the complete txt
        """
        pos = txt.rfind('\n')
        prev_pos = len(txt)
        maxloop = 10
        while pos >= 0:
            segment = txt[pos:prev_pos].strip()
            if segment:
                break
            # print (pos, repr(segment))
            prev_pos = pos
            pos = txt.rfind('\n', 0, pos-1)
            maxloop -= 1
            if maxloop < 0:
                break
        return segment

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
    @option('--indent', type=int, global_option=True)
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        self._yaml = YAML(self._args, self._config)
        if self._args.func:
            return self._args.func()

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
    @option('--save', action='store_true', help="""save the rewritten data back
    to the input file (if it doesn't exist a '.orig' backup will be made)
    """)
    @option('file', nargs='+')
    def rt(self):
        return self._yaml.round_trip()

    @sub_parser(
        aliases=['from-json'],
        help='convert json to block YAML',
        description='convert json to block YAML',
    )
    @option('--flow', action='store_true',
            help='use flow instead of block style')
    @option('file', nargs='+')
    def json(self):
        return self._yaml.from_json()

    @sub_parser(
        aliases=['from-ini'],
        help='convert .ini/config to block YAML',
        description='convert .ini/config to block YAML',
    )
    @option('--basename', '-b', action='store_true',
            help='re-use basename of file for .yaml file, instead of writing'
            ' to stdout')
    @option('file')
    def ini(self):
        return self._yaml.from_ini()

    @sub_parser(
        #aliases=['to-html'],
        help='convert YAML to html tables',
        description="""convert YAML to html tables. If hierarchy is two deep (
        sequence/mapping over sequence/mapping) this is mapped to one table
        If the hierarchy is three deep, a list of 2 deep tables is assumed, but
        any non-list/mapp second level items are considered text.
        Row level keys are inserted in first column (unless --no-row-key),
        item level keys are used as classes for the TD.
        """,
    )
    @option("--level", action='store_true', help="print # levels and exit")
    @option('file')
    def htmltable(self):
        return self._yaml.to_htmltable()

    @sub_parser('from-html',
        help='convert HTML to YAML',
        description="""convert HTML to YAML. Tags become keys with as
        value a list. The first item in the list is a key value pair with
        key ".attribute" if attributes are available followed by tag and string
        segment items. Lists with one item are by default flattened.
        """,
    )
    @option("--no-body", action='store_true',
            help="drop top level html and body from HTML code segments")
    @option("--strip", action='store_true',
            help="strip whitespace surrounding strings")
    @option('file')
    def from_html(self):
        return self._yaml.from_html()

    @sub_parser('from-csv',
        aliases=['csv'],
        help='convert CSV to YAML',
        description="""convert CSV to YAML.
        By default generates a list of rows, with the items in a 2nd level
        list.
        """,
    )
    @option('--delimiter')
    #@option('--quotechar')
    @option('file')
    def from_csv(self):
        return self._yaml.from_csv()

    if 'test' in sys.argv:
        @sub_parser(
            description='internal test function',
        )
        @option('file', nargs='*')
        def test(self):
            return self._yaml.test()


def main():
    n = YAML_Cmd()
    n.parse_args()
    sys.exit(n.run())

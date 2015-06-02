# coding: utf-8

from __future__ import print_function

"""
conversion helpers for yaml utility to/from HTML

html/xml to yaml inspired by
http://programmers.stackexchange.com/questions/157395/yaml-translating-free-flowing-text-from-xml

"""

import sys


class HTML2YAML(object):
    def __init__(self, args=None):
        self.flatten = not getattr(args, 'no_flatten', False)
        self.strip = getattr(args, 'strip', False)
        self.no_body = getattr(args, 'no_body', False)

    def __call__(self, html):
        d = self.html_to_data(html)
        if self.no_body:
            d = d['html']['body']
        return self.data_to_yaml(d)

    def data_to_yaml(self, d):
        import ruamel.yaml
        return ruamel.yaml.dump(
            d,
            Dumper=ruamel.yaml.RoundTripDumper
        )

    def html_to_data(self, html):
        try:
            import bs4
        except ImportError:
            print("For HTML conversion you need to install BeautifulSoup")
            print("e.g. using (pip install beautifulsoup4)")
            sys.exit(1)

        soup = bs4.BeautifulSoup(html)
        data = self._convert_node(soup)
        return data

    def _convert_node(self, node, depth=0):
        try:
            import bs4
        except ImportError:
            print("For HTML conversion you need to install BeautifulSoup")
            print("e.g. using (pip install beautifulsoup4)")
            sys.exit(1)
        from ruamel.yaml.comments import CommentedMap
        from ruamel.yaml.scalarstring import PreservedScalarString
        ret_val = []
        if node.attrs:
            ret_val.append({'.attribute': node.attrs})
        for data in node.contents:
            if isinstance(data, bs4.Tag):
                kv = CommentedMap()
                #print data.name, data.attrs
                # convert the intenals of the tag
                kv[data.name] = self._convert_node(data, depth+1)
                ret_val.append(kv)
            elif isinstance(data, bs4.NavigableString):
                s, nl = self._strip(data)
                if not s:
                    continue
                if nl:
                    ret_val.append(PreservedScalarString(s))
                    continue
                ret_val.append(s)
            else:
                print('unknow type', type(data))
        if self.flatten and len(ret_val) == 1:
            return ret_val[0]
        return ret_val

    def _strip(self, data):
        import textwrap
        # multiline strings might be nicely formatted so don't
        # use .strip() immediately
        if self.strip:
            s = data.strip()
        else:
            s = data.rstrip()
        if not s:
            return None, False
        first_nl_pos = s.find(u'\n')
        if first_nl_pos < 0:
            return s, False
        if not s[:first_nl_pos].strip():  # i.e. space until first newline
            if u'\n' not in s[first_nl_pos+1:]:
                print(repr(data), repr(s))
                # single line of text preceded and followed by nl
                return s.strip(), False
            # use data here, removing the final newline would get your |- as marker
            s = textwrap.dedent(data[first_nl_pos+1:])
        return s, True


class YAML2HTML(object):
    def __init__(self, args=None):
        pass

    def __call__(self, yaml):
        d = self.yaml_to_data(yaml)
        return self.data_to_html(d)

    def data_to_html(self, d):
        if isinstance(d, dict):
            pass

    def yaml_to_data(self, yaml):
        import ruamel.yaml
        return ruamel.yaml.load(yaml)
        return data


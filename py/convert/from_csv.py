# coding: utf-8

from __future__ import print_function

import dateutil.parser
import ruamel.yaml

class CSV2YAML(object):
    def __init__(self, args=None):
        # self.flatten = not getattr(args, 'no_flatten', False)
        self.delimiter = getattr(args, 'delimiter', None)

    def __call__(self, csv_file_name):
        import csv

        data = []
        with open(csv_file_name) as inf:
            for line in csv.reader(inf, delimiter=self.delimiter):
                data.append(self.process_line(line))
        print(ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper))

    def process_line(self, line):
        """convert lines, trying, int, float, date"""
        ret_val = []
        for elem in line:
            try:
                res = int(elem)
                ret_val.append(res)
                continue
            except ValueError:
                pass
            try:
                res = float(elem)
                ret_val.append(res)
                continue
            except ValueError:
                pass
            try:
                res = dateutil.parser.parse(elem)
                ret_val.append(res)
                continue
            except TypeError:
                pass
            ret_val.append(elem)
        return ret_val


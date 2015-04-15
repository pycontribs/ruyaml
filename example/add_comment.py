from __future__ import print_function

import ruamel.yaml

inp = """\
abc:
  - a     # comment 1
xyz:
  a: 1    # comment 2
  b: 2
  c: 3
  d: 4
  e: 5
  f: 6 # comment 3
"""

data = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)
data['abc'].append('b')
data['abc'].yaml_add_eol_comment('comment 4', 1)  # takes column of comment 1
data['xyz'].yaml_add_eol_comment('comment 5', 'c')  # takes column of comment 2
data['xyz'].yaml_add_eol_comment('comment 6', 'e')  # takes column of comment 3
data['xyz'].yaml_add_eol_comment('comment 7', 'd', column=20)

print(ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper), end='')

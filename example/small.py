from __future__ import print_function

import ruamel.yaml

inp = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
"""

code = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)
code['name']['given'] = 'Bob'

print(ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper), end='')

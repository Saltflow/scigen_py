import sys
sys.path.append(".")

import read_rules

def test_read_rules(file):
  with open(file, 'r') as f:
    fh = f.readlines()
  rules = {}
  RE = None
  read_rules.read_rules(fh, rules, RE, 10)
  print(rules)
  print(RE)

test_read_rules("scirules.in")
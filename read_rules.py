from logging import warn, warning
import os
import re
import random

from numpy import append


def file_name(filename):
  return filename + ".file"

def dup_name(name):
  return name + "!!!"

def read_rules(fh, rules, RE, debug):
  line_num = 0
  while(line_num < len(fh)):
    print(line_num)
    line = fh[line_num]
    line_num += 1
    if(line[0] == '#'):
      continue
    if(not re.match("\S", line)):
      continue
    word = line.split()
    name = word[0]
    rule = ""

    if(name[-1] == '!'):
      rules[dup_name(name)] = ''
    
    if(name == '.include'):
      file = word[1]

      if(file_name(file) in rules.keys()):
        if(debug > 0):
          print ("Skipping duplicate included file $file\n")
          continue
        else:
          rules[file_name(file)] = 1
      with open(file, 'r') as f:
        inc_fh = f.readlines()
      read_rules(inc_fh, rules, None, debug)
      continue

    if(len(word) >= 2 and word[1] == '{'): # name included
      end = 0
      while(line_num < len(fh)):
        line_num += 1
        line =fh[line_num]
        if(re.match("^}[\r\n]+$", line)):
          end = 1
          break
        else:
          rule += line.rstrip()
      if(not end):
        print(name, "EOF found before close rule")
    else:
      line_rm_trailing = ' '.join(line.split()[1:])
      rule = line_rm_trailing.rstrip()

    weight = 1
    name_by_weight = re.match("([^\+]*)\+(\d+)$", name)
    if(name_by_weight):
      name = name_by_weight.group(1)
      weight = eval(name_by_weight.group(2))
      if(debug > 10):
        warning(f"weighting rule by {weight}: {name} {rule}\n")
    
    while(weight > 0):
      weight = weight - 1
      if(name == "\n"):
        print(word)
      if(name not in rules.keys()):
        rules[name] = []
      rules[name].append(rule)
  if(RE is not None):
    return compute_re(rules, RE)

def compute_re(rules, RE):
  in_str = '|'.join(sorted(rules.keys(), key= lambda x:-len(x)))
  RE = f"^(.*?)({in_str})"
  return RE
  
def expand(rules, start, RE, debug):
  # check for special rules ending in + and # 
  # Rules ending in + generate a sequential integer
  # The same rule ending in # chooses a random # from among preiously
  # generated integers
  start_match = re.match("(.*)\+$", start)
  if(start_match):
    rule = start_match.group(1)
    i = rules[rule]
    if(not i):
      i = 0
      rules[rule] = 1
    else:
      rules[rule] = i+1
    return i

  start_match = re.match("(.*)\#$", start)
  if(start_match):
    rule = start_match.group(1)
    i = rules[rule]
    if(not i):
      i = 0
    else:
      i = random.randint(eval(i))
    return str(i)

  repeat = 1
  count = 0
  components = []
  while(repeat):
    input = pick_rand(rules[start])
    count += 1
    if(debug >= 5):
      warn(f"{start} -> {input}")
    
    repeat = 0
    while(True):
      first_rule = pop_first_rule(rules, input, RE)
      if(first_rule is None):
        break
      pre, rule, input = first_rule
      ex = expand(rules, rule, RE, debug)
      if(len(pre)):
        components.append(pre)
      if(len(ex)):
        components.append(ex)
    if(len(input)):
      components.append(input)
    full_token = "".join(components)
    if (dup_name(start) in rules.keys()):
      ref = rules[dup_name(start)]
      dups = ref
      for d in dups:
        if(d == full_token):
          repeat = 1
      if (not repeat):
        rules[dup_name(start)] += full_token
      elif count > 50:
        repeat = 0
  return full_token
    

      
def pop_first_rule(rules, input, RE): # rule and preamble are outputs
  input_match = re.match(RE, input)
  if(input_match):
    preamble = input_match.group(1)
    rule = input_match.group(2)
    input_new = input[len(preamble) + len(rule):]
    return preamble, rule, input_new
  return None

def pick_rand(in_set):
  return in_set[random.randint(0, len(in_set) - 1)]

def generate(rules, start, RE, debug, pretty):
  s = expand(rules, start, RE, debug)
  return s
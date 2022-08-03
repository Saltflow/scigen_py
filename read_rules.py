from logging import warning
import os
import re
import random


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
      rules['dup_name'].append(dup_name(name))
    
    if(name == '.include'):
      file = word[1]

      if(file in rules['file']):
        if(debug > 0):
          print ("Skipping duplicate included file $file\n")
          continue
        else:
          rules['file'].append(file)
      with open(file, 'r') as f:
        inc_fh = f.readlines()
      read_rules(inc_fh, rules, None, debug)
    if(len(word) >= 2 and word[1] == '{'): # name included
      end = 0
      while(line_num < len(fh)):
        line_num += 1
        line =fh[line_num]
        if(re.match("^}[\r\n]+$", line)):
          end = 1
          break
        else:
          rule += line
      if(not end):
        print(name, "EOF found before close rule")
    else:
      line_rm_trailing = re.match("^\S+\s+", line).group()
      rule = line_rm_trailing.rstrip('\n')

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
      rules['name'].append(name)
  if(RE is not None):
    compute_re(rules, RE)

def compute_re(rules, RE):
  in_str = '|'.join(rules['name'].sort(key=lambda x: len(x)))
  RE = list(f"^(.*?)({in_str})")
  
def expand(rules, start, RE, debug):
  pass
      
def pop_first_rule(rules, input, RE): # rule and preamble are outputs
  input_match = re.match(RE, input)
  if(input_match):
    preamble = input_match.group(1)
    rule = input_match.group(2)
    return preamble, rule
  return None

def pick_rand(in_set):
  return in_set[random.randint(0, len(in_set) - 1)]

def generate(rules, start, RE, debug, pretty):
  s = expand(rules, start, RE, debug)
  return s
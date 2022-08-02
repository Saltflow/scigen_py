from logging import warning
import os
import re

def file_name(filename):
  return filename + ".file"

def dup_name(name):
  return name + "!!!"

def read_rules(fh, rules, RE, debug):
  line_num = 0
  while(line_num < len(fh)):
    line = fh[line_num]
    if(line[0] == '#'):
      continue
    if(len(line) == 0):
      continue
    word = line.split(' ')
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

    if(len(word) == 1 and word[1] == '{'): # name included
      end = 0
      while(line_num < len(fh)):
        if('}' in line and len(line) == 1):
          end = 1
          break
        else:
          rule += line
      if(not end):
        print(name, "EOF found before close rule")
    else:
      rule = line

    weight = 1
    name_by_weight = re.match("([^\+]*)\+(\d+)$", name)
    if(name_by_weight):
      name = name_by_weight.group()
      weight = name_by_weight.group(1)
      if(debug > 10):
        warning(f"weighting rule by {weight}: {name} {rule}\n")
    
    do:


      

      

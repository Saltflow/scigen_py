import sys
sys.path.append(".")

from read_rules import generate, read_rules

start_rule = "SCIPAPER_LATEX"
file = "scirules.in"
sys_name = "HARPOON"
with open(file, 'r') as f:
  tex_fh = f.readlines()

tex_data = {}
RE = []
RE = read_rules(tex_fh, tex_data, RE, 10)

tex = generate(tex_data, start_rule, RE, 10, 0)

print(tex)
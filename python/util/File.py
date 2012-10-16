from __future__ import absolute_import, division, print_function, unicode_literals

import yaml

from contextlib import closing

import os.path

def open_userfile(fname, perms='r'):
  return open(os.path.expanduser(fname), perms)

def yaml_load_all(fname, report_error=True):
  opened = False
  try:
    f = open_userfile(fname, 'r')
  except:
    if report_error:
      print("Can't read filename", fname)
    return []

  with closing(f):
    return list(yaml.safe_load_all(f))

def yaml_dump_all(fname, *items):
  try:
    with closing(open_userfile(fname, 'w')) as f:
      yaml.safe_dump_all(f, items)
  except:
    print("Can't write filename", fname)

def yaml_load(fname, report_error=False):
  y = yaml_load_all(fname, report_error)
  if y:
    return y[0]
  else:
    return {}

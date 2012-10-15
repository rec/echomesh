from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing
import os.path

def open_userfile(fname, perms='r'):
  return open(os.path.expanduser(fname), perms)

def yaml_load_all(fname):
  try:
    with closing(open_userfile(fname)) as f:
      return list(yaml.safe_load_all(f))
  except:
    print("Can't read filename", fname)
    return []

def yaml_dump_all(fname, *items):
  try:
    with closing(open_userfile(fname, 'w')) as f:
      yaml.safe_dump_all(f, items)
  except:
    print("Can't write filename", fname)

def yaml_load(fname):
  y = yaml_load_all(fname)
  if y:
    return y[0]
  else:
    return {}

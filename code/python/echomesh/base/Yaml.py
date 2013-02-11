from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import yaml

from contextlib import closing

def _open_userfile(fname, perms='r'):
  return open(os.path.expanduser(fname), perms)

def encode_one(item):
  return yaml.safe_dump(item)

def decode(s):
  return list(yaml.safe_load_all(s))

def decode_one(s):
  return yaml.safe_load(s)

def read(fname, allow_empty=True):
  opened = False
  try:
    f = _open_userfile(fname, 'r')
  except:
    if allow_empty:
      return None
    else:
      raise

  with closing(f):
    return decode(f)

def write(fname, *items):
  try:
    with closing(_open_userfile(fname, 'w')) as f:
      yaml.safe_dump_all(items, f)
  except Exception as e:
    print("Can't write filename", fname, e.message)


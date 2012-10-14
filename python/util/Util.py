from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

LOG_NEW_FILE = False

def get_and_increment_index_file(f, open=open):
  index = '0'
  try:
    with closing(open(f)) as input:
      index = str(1 + int(input.read()))
  except:
    if LOG_NEW_FILE:
      print('Creating index file', f)

  with closing(open(f, 'w')) as output:
    output.write(index)
  return index


def level_slot(level, levels):
  for i, lev in enumerate(levels):
    if level < lev:
      return i
  return len(levels)


def call_if_different(callback, initial=None):
  old_val = [initial]
  def cb(value):
    if value != old_val[0]:
      old_val[0] = value
      callback(value)
  return cb


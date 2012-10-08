#!/usr/bin/python

ELLIPSIS = '...'
LOG_NEW_FILE = False

def truncate(s, length, ellipsis=ELLIPSIS):
  if length < len(s):
    if length < len(ellipsis):
      s = ellipsis
    else:
      s = s[0:length - len(ellipsis)] + ellipsis

  return s[0:length]

def truncate_suffix(s, suffix, length, ellipsis=ELLIPSIS):
  suffix = suffix[0:length]
  return truncate(s, length - len(suffix), ellipsis) + suffix


def get_and_increment_index_file(f, open=open):
  index = '0'
  try:
    with open(f) as input:
      index = str(1 + int(input.read()))
  except:
    if LOG_NEW_FILE:
      print 'Creating index file', f

  with open(f, 'w') as output:
    output.write(index)
  return index


if __name__ == "__main__":
  import doctest
  doctest.testmod()

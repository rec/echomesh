from __future__ import absolute_import, division, print_function, unicode_literals

import re
import six

WORD_SPLITTER = re.compile(r'[,\s]+')  # But no "." , which is used in filenames.

def split_words(s):
  return [i for i in WORD_SPLITTER.split(s) if i]

def pair_split(items, split='as'):
  result = []
  queue, parts = [], []
  for item in items:
    if item.lower() == split:
      if queue or not parts:
        raise Exception('Couldn\'t correctly understand %s" in %s' % (split, items))
      queue, parts = parts, []
    elif queue:
      result.append((queue.pop(0), item))
    else:
      parts.append(item)
  result.extend((s, None) for s in queue + parts)
  return result

def split_scores(scores):
  if not scores:
    return []

  if isinstance(scores, (tuple, list)):
    scores = ' '.join(scores)
  return pair_split(split_words(scores))

def split_args(args):
  address = []
  value = None
  equals_found = False
  for arg in args:
    if equals_found:
      yield address, arg
      address = []
      equals_found = False
      continue
    if '=' in arg:
      name, value = arg.split('=', 1)
      equals_found = True
    else:
      name, value = arg, None

    name = name.strip().strip(':')
    if name:
      address.append(name)

    if value:
      yield address, value
      address = []

  if address:
    print('ERROR: Extra arguments at the end: "%s".' % ' '.join(address))

def split_args_to_dict(args):
  result = {}
  for address, value in split_args(args):
    last = address.pop()
    res = result
    for a in address:
      res = res.setdefault(a, {})
    res[last] = value
  return result

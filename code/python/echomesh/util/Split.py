from __future__ import absolute_import, division, print_function, unicode_literals

import re
WORD_SPLITTER = re.compile(r'[,\s]+')

def split_words(s):
  return [i for i in WORD_SPLITTER.split(s) if i]

def pair_split(items, split='as'):
  result = []
  queue, parts = [], []
  for item in items:
    if item.lower() == split:
      if queue or not parts:
        raise Exception('Couldn\'t correctly understand %s" in %s' %
                        (split, items))
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
  return  pair_split(split_words(scores))


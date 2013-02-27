from __future__ import absolute_import, division, print_function, unicode_literals

import re
import six

WORD_SPLITTER = re.compile(r'[,\s]+')  # But no "." , which is used in filenames.

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def split_words(s):
  return [i for i in WORD_SPLITTER.split(s) if i]

def split_list(parts, splitter):
  if splitter in parts:
    loc = parts.index(splitter)
    return parts[0:loc], parts[loc + 1:]
  else:
    return parts, []

def split_scores(scores):
  if not scores:
    return [], None
  if isinstance(scores, six.string_types):
    score_list = split_words(scores)
  else:
    score_list = scores
  if isinstance(score_list[0], six.string_types):
    return split_list(score_list, 'as')
  if len(scores) == 1:
    return scores[0], None
  if len(scores) == 2:
    return scores
  raise Exception("Didn't understand scores config: %s" % scores)

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

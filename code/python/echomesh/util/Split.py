from __future__ import absolute_import, division, print_function, unicode_literals

import re
import six

WORD_SPLITTER = re.compile(r'[,\s]')  # But no "." , which is used in filenames.

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def split_words(s):
  split = WORD_SPLITTER.split(s)

  # Remove first or last if blank.
  for i in [-1, 0]:
    split[i] or split.pop(i)

  return split

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

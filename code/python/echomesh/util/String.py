from __future__ import absolute_import, division, print_function, unicode_literals

def join_words(*words):
  if not words:
    return ''
  if len(words) == 1:
    return words[0]

  if len(words) == 2:
    return '%s and %s' % words

  return '%s, and %s' % (', '.join(words[:-1]), words[-1])

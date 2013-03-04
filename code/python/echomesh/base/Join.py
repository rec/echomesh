from __future__ import absolute_import, division, print_function, unicode_literals

def join_words(words, format=''):
  words = sorted(words)
  if not words:
    return ''
  if format:
    if '%s' not in format:
      format = '%s%%s%s' % (format, format)
    words = [format % w for w in words]
  if len(words) == 1:
    return words[0]
  if len(words) == 2:
    return ' and '.join(words)
  return '%s, and %s' % (', '.join(words[:-1]), words[-1])

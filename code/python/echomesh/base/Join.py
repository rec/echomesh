from __future__ import absolute_import, division, print_function, unicode_literals

def join_words(words, fmt=''):
  words = sorted(words)
  if not words:
    return ''
  if fmt:
    if '%s' not in fmt:
      fmt = '%s%%s%s' % (fmt, fmt)
    words = [fmt % w for w in words]
  if len(words) == 1:
    return words[0]
  if len(words) == 2:
    return ' and '.join(words)
  return '%s, and %s' % (', '.join(words[:-1]), words[-1])

def join_file_names(file_names):
  if len(file_names) == 1:
    return 'file %s' % file_names[0]
  else:
    return 'files %s' % join_words(file_names)


from __future__ import absolute_import, division, print_function, unicode_literals

ELLIPSIS = '...'

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

from __future__ import absolute_import, division, print_function, unicode_literals

K = 1024
NAMES = '', 'K', 'M', 'G'

def size_name(bytes):
  for name in NAMES:
    if bytes < K or name == NAMES[-1]:
      return str(int(bytes)) + name
    bytes = round(bytes / K)


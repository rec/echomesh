from __future__ import absolute_import, division, print_function, unicode_literals

K = 1024
NAMES = '', 'K', 'M', 'G'

def size_name(byte_count):
  for name in NAMES:
    if byte_count < K or name == NAMES[-1]:
      return str(int(byte_count)) + name
    byte_count = round(byte_count / K)


from __future__ import absolute_import, division, print_function, unicode_literals

def split_flag(flag):
  parts = flag.lstrip('-').split('=', 1)
  flag = parts.pop(0)
  return flag, parts[0] if parts else ''



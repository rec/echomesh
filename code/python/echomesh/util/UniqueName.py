from __future__ import absolute_import, division, print_function, unicode_literals

import re

MATCH_NAME = re.compile(r'(.*)\.(\d+)$')

def unique_name(name, elements):
  while name in elements:
    match = MATCH_NAME.match(name)
    if match:
      base, suffix = match.groups()
      suffix = 1 + int(suffix)
    else:
      base, suffix = name, 1
    name = '%s.%d' % (base, suffix)

  return name


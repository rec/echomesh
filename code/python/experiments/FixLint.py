#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import re
import sys

MATCH_ERROR = re.compile(r'(\w\d{4}):\s*(\d+),(-?\d+):(.*)')

error_file = ''

for line in sys.stdin:
  if line.startswith('*************'):
    parts = line.split()
    if len(parts) == 3:
      error_file = '%s.py' % parts[2].replace('.', '/')
  else:
    match = MATCH_ERROR.match(line)
    if match:
      code, line_number, column, error = match.groups()
      line = '%s:%s:%s: error: %s: %s'  % (
        error_file, line_number, column, code, error)

  print(line)


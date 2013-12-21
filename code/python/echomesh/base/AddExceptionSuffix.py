from __future__ import absolute_import, division, print_function, unicode_literals

import sys

def add_exception_suffix(*suffixes):
  e = sys.exc_info()[1]
  suffix = ' '.join(suffixes)
  e.args = tuple(str(a) + suffix for a in getattr(e, 'args', ()))
  raise

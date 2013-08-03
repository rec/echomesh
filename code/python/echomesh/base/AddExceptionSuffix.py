from __future__ import absolute_import, division, print_function, unicode_literals

def add_exception_suffix(e, *suffixes):
  # TODO: use traceback.
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)

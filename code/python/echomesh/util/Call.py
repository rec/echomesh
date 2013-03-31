from __future__ import absolute_import, division, print_function, unicode_literals

import six

def call(f):
  while six.callable(f):
    f = f()
  return f

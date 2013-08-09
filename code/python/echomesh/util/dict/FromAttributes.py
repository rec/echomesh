from __future__ import absolute_import, division, print_function, unicode_literals

def from_attributes(object, fields):
  return dict((f, getattr(object, f, None)) for f in fields)


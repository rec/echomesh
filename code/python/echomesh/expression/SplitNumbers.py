from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.expression import Units

def split(items):
  kwds = {}
  numeric = []
  for k, v in six.iteritems(items):
    if isinstance(k, six.string_types) and k[0].isalpha():
      kwds[k] = v
    else:
      numeric.append([Units.convert(k), Units.convert(v)])
  return kwds, sorted(numeric)

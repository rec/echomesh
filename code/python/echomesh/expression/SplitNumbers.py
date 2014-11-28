from __future__ import absolute_import, division, print_function, unicode_literals

import six

def split(items):
    kwds = {}
    numeric = []
    for k, v in six.iteritems(items):
        if isinstance(k, six.string_types) and k[0].isalpha():
            kwds[k] = v
        else:
            from echomesh.expression import Expression
            numeric.append([Expression.convert(k), Expression.convert(v)])
    return kwds, sorted(numeric)

"""

>>> table_to_parts({})
[]

>>> table_to_parts({'a': 1})
[[[u'a'], 1]]

>>> sorted(table_to_parts({'a': 1, 'b': 2}))
[[[u'a'], 1], [[u'b'], 2]]

>>> sorted(table_to_parts({'a': 1, 'b': {'c': 3, 'd': {'e': 4}}}))
[[[u'a'], 1], [[u'b', u'c'], 3], [[u'b', u'd', u'e'], 4]]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml
from echomesh.base.MergeConfig import table_to_parts

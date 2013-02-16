from __future__ import absolute_import, division, print_function, unicode_literals

try:
  from weakref import WeakSet

except:
  from .weakrefset import WeakSet

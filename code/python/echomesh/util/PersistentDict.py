from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class PersistentDict(dict):
  def __init__(self, filename=''):
    super(PersistentDict, self).__init__()
    self._filename = filename
    if filename:
      original = Yaml.read(self._filename)
      if original:
        super(PersistentDict, self).update(original[0])

  def set_filename(self, filename):
    self._filename = filename
    self._write()

  def _write(self):
    Yaml.write(self._filename, self)

  def __delitem___(self, key):
    super(PersistentDict, self).__delitem___(key)
    self._write()

  def __setitem__(self, key, value):
    super(PersistentDict, self).__setitem__(key, value)
    self._write()

  def clear(self):
    super(PersistentDict, self).clear()
    self._write()

  def pop(self, *args, **kwds):
    x = super(PersistentDict, self).pop(*arg, **kwds)
    self._write()
    return x

  def popitem(self, *args, **kwds):
    x = super(PersistentDict, self).popitem(*arg, **kwds)
    self._write()
    return x

  def setdefault(self, *args, **kwds):
    super(PersistentDict, self).setdefault(*arg, **kwds)
    self._write()

  def update(self, *args, **kwds):
    super(PersistentDict, self).update(*arg, **kwds)
    self._write()




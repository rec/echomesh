from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.Expression import Expression
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def set_player(self, element, level=1, pan=0, loops=1, **kwds):
  self.element = element
  self.file = kwds.pop('file')
  if kwds:
    LOGGER.error('Unused keywords %s', kwds)
  self.passthrough = (level == 1 and pan == 0)

  self.level = Expression(level, element)
  self.pan = Expression(pan, element)
  self.loops = loops

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import make_output
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Remap(Output):
  def __init__(self, description):
    remap = description.pop('map', None)
    if remap is None:
      LOGGER.error('No map in output Remap')
    remap = remap or {}
    self.length = 1 + max(0, *remap.keys())

    self.remap = {}
    for k, v in remap.items():
      self.remap.setdefault(k, []).append(v)

    self.finish_construction(description)

  def emit_output(self, data):
    old_data, data = data, [None] * max(self.length, len(data))
    for i, x in enumerate(old_data):
      slots = self.remap.get(i)
      if slots is None:
        data[i] = x
      else:
        for s in slots:
          data[s] = x
    super(Remap, self).emit_output(data)

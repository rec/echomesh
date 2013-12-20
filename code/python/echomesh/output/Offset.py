from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import make_output
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Offset(Output):
  def __init__(self, description):
    self.offset = description.pop('offset', None)
    if self.offset is None:
      LOGGER.error('No offset in output Offset')
      self.offset = 0

  def emit_output(self, data):
    if self.offset > 0:
      data = [None] * self.offset + data
    else:
      data = data[-self.offset:]
    super(Offset, self).emit_output(data)

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.Registry import make_output
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Offset(Output):
    def __init__(self, offset=None, length=-1, **description):
        super(Offset, self).__init__()
        self.offset = offset
        if self.offset is None:
            LOGGER.error('No offset in output Offset')
            self.offset = 0
        self.length = length
        super(Offset, self).finish_construction(description)

    def emit_output(self, data):
        if self.offset > 0:
            data = [None] * self.offset + data
        else:
            data = data[-self.offset:]
        if self.length >= 0:
            data = data[:self.length]
        super(Offset, self).emit_output(data)

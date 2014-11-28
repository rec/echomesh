from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Bidirectional(Output):
    def __init__(self, start_forward=True, width=0, **description):
        super(Bidirectional, self).__init__()
        self.start_forward = start_forward
        self.width = width
        if not width:
            LOGGER.error('No width in output Bidirectional')

        self.finish_construction(description)

    def emit_output(self, data):
        if self.width:
            begin = self.width if self.start_forward else 0
            while begin < len(data):
                end = begin + self.width
                data[begin:end] = reversed(data[begin:end])
                begin += 2 * self.width

        super(Bidirectional, self).emit_output(data)

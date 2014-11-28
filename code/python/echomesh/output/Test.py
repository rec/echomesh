from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.Output import Output

class Test(Output):
    def emit_output(self, data):
        self.data = data

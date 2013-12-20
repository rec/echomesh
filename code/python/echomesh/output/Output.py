from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import make_output
from echomesh.util import Log


LOGGER = Log.logger(__name__)

class Output(object):
  def finish_construction(self, description, is_redirect=True):
    if is_redirect:
      output = description.pop('output', None)
      if output is None:
        raise Exception('No output in %s' % self.__class__.__name__)
      if not isinstance(output, (list, tuple)):
        output = [output]

      self.output = [make_output(o) for o in output]
    else:
      self.output = []

    if description:
      LOGGER.error('Unknown keywords %s in output %s', description,
                   self.__class__.__name__)

  def emit_output(self, data):
    for o in self.output:
      o.emit_output(data)

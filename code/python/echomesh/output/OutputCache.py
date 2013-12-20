from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile

from echomesh.util import Log
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

class _SingleOutput(object):
  def __init__(self, filename, output_cache):
    from echomesh.output import make_output
    self._filename = filename
    self._output = make_output(filename)
    self._output_cache = output_cache

  def __getattr__(self, name):
    return getattr(self._output, name)

  def __del__(self):
    try:
      self._output_cache.remove_output(self._filename)
    except:
      LOGGER.error('Unexpected error in _SingleOutput.__del__')


class OutputCache(object):
  def __init__(self):
    self.outputs = {}
    self.lock = Lock.Lock()

  def add_output(self, name):
    with self.lock:
      filename = DataFile.resolve('output', name)
      if not filename:
        raise Exception('No output named "%s".' % name)
      output = self.outputs.get(filename, [None, 0])
      output[1] += 1
      if not output[0]:
        output[0] = _SingleOutput(filename, self)
        self.outputs[filename] = output
      return output[0]

  def remove_output(self, filename):
    with self.lock:
      output = self.outputs[filename]
      output[1] -= 1


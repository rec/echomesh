from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile

from echomesh.util import Log
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

def default_output():
  from echomesh.output.Visualizer import Visualizer
  return Visualizer()

class _SingleOutput(object):
  def __init__(self, name, data, output_cache):
    from echomesh.output import make_output
    self._name = name
    self._output_cache = output_cache
    if data:
      from echomesh.output import make_output
      self._output = make_output(data)
    else:
      self._output = default_output()
    self._output.start()

  def __getattr__(self, name):
    return getattr(self._output, name)

  def __del__(self):
    try:
      self._output_cache.remove_output(self._name)
    except:
      LOGGER.error('Unexpected error in _SingleOutput.__del__')

class OutputCache(object):
  def __init__(self):
    self.outputs = {}
    self.lock = Lock.Lock()

  def get_output(self, name):
    with self.lock:
      output = self.outputs.setdefault(name, [None, 1])
      if output[0]:
        output[1] += 1
      else:
        if name:
          try:
            data = DataFile.load('output', name)
          except:
            try:
              from echomesh.output.Registry import REGISTRY
              data = {'type': REGISTRY.entry(name).name}
            except:
              del self.outputs[name]
              raise Exception('No output named "%s".' % name)
        else:
          data = None
        output[0] = _SingleOutput(name, data, self)
        self.outputs[name] = output
      return output[0]

  def remove_output(self, name):
    with self.lock:
      output = self.outputs[name]
      output[1] -= 1

  def pause(self):
    with self.lock:
      for output in self.outputs.values():
        output[0].pause()


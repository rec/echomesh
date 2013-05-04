from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy

from echomesh.color import ColorTable
from echomesh.color.LightBank import LightBank
from echomesh.network import ClientServer
from echomesh.util import Quit

class ExternalLightBank(LightBank):
  def __init__(self):
    self.process = None
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    ClientServer.instance()
    super(ExternalLightBank, self)._before_thread_start()

  def shutdown(self):
    if not Quit.QUITTING:
      ClientServer.instance().write(type='hide')

  def clear(self):
    with self.lock:
      ClientServer.instance().write(type='clear')

  def config_update(self, get):
    super(ExternalLightBank, self).config_update(get)
    light = copy.deepcopy(get('light'))
    visualizer = light['visualizer']
    visualizer['background'] = ColorTable.to_color(visualizer['background'])

    dl = visualizer['instrument']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    with self.lock:
      ClientServer.instance().set_config(
        {'type': 'config', 'data': light},
        {'type': 'show'})

  def _after_thread_pause(self):
    if not Quit.QUITTING:
      super(ExternalLightBank, self)._after_thread_pause()
      self.shutdown()

  def _display_lights(self):
    with self.lock:
      bytes = _split_long_strings(base64.b64encode(self.bytes))
      ClientServer.instance().write(type='light', data=bytes)


# Fix for https://github.com/rec/echomesh/issues/342
_LONGEST_STRING = 3000

def _split_long_strings(s):
  result = []
  while len(s) > _LONGEST_STRING:
    result.append(s[0:_LONGEST_STRING])
    s = s[_LONGEST_STRING:]
  result.append(s)
  return result

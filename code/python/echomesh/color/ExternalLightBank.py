from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy

from echomesh.color import ColorTable
from echomesh.color.LightBank import LightBank
from echomesh.network import ClientServer
from echomesh.util import Log
from echomesh.util import Quit

LOGGER = Log.logger(__name__)

class ExternalLightBank(LightBank):
  def __init__(self):
    self.process = None
    self.failed = False
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    ClientServer.instance()
    super(ExternalLightBank, self)._before_thread_start()

  def _fail(self):
    LOGGER.error()
    self.failed = True
    if self.visualizer_closes_echomesh:
      exit(0)

  def shutdown(self):
    if not (Quit.QUITTING or self.failed):
      try:
        ClientServer.instance().write(type='hide')
      except:
        self._fail()

  def clear(self):
    with self.lock:
      if not self.failed:
        try:
          ClientServer.instance().write(type='clear')
        except:
          self._fail()

  def config_update(self, get):
    super(ExternalLightBank, self).config_update(get)
    light = copy.deepcopy(get('light'))
    visualizer = light['visualizer']
    self.visualizer_closes_echomesh = visualizer['visualizer_closes_echomesh']
    visualizer['background'] = ColorTable.to_color(visualizer['background'])

    dl = visualizer['instrument']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    config = {'light': light, 'midi': get('midi')}

    with self.lock:
      ClientServer.instance().set_config({'type': 'config', 'data': config})

  def _after_thread_pause(self):
    if not Quit.QUITTING:
      try:
        super(ExternalLightBank, self)._after_thread_pause()
      except:
        self._fail()
      try:
        self.shutdown()
      except:
        self._fail()

  def _display_lights(self):
    with self.lock:
      if self.failed:
        return
      bytes = _split_long_strings(base64.b64encode(self.bytes))
      try:
        ClientServer.instance().write(type='light', data=bytes)
      except:
        self._fail()


# Fix for https://github.com/rec/echomesh/issues/342
_LONGEST_STRING = 3000

def _split_long_strings(s):
  result = []
  while len(s) > _LONGEST_STRING:
    result.append(s[0:_LONGEST_STRING])
    s = s[_LONGEST_STRING:]
  result.append(s)
  return result

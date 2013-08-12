from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy

from echomesh.base import Quit
from echomesh.color import ColorTable
from echomesh.expression import Expression
from echomesh.light.SpiLightBank import SpiLightBank
from echomesh.network import ClientServer
from echomesh.util import Log
from echomesh.util.string import Split

LOGGER = Log.logger(__name__)

_LONGEST_STRING = 3000

class ExternalLightBank(SpiLightBank):
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
    if self.closes_echomesh:
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
    light['brightness'] = Expression.convert(light['brightness'])
    light['hardware']['period'] = Expression.convert(light['hardware']['period'])
    light['visualizer']['period'] = Expression.convert(light['visualizer']['period'])
    visualizer = light['visualizer']
    self.closes_echomesh = visualizer['closes_echomesh']
    visualizer['background'] = ColorTable.to_color(visualizer['background'])

    dl = visualizer['instrument']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    data = {'light': light, 'midi': get('midi')}
    config = {'type': 'config', 'data': data}

    LOGGER.debug('The server connected to the client and is about to send a '
                 + 'configuration looking like this: %s', config)
    with self.lock:
      LOGGER.debug('The server took the client/server lock')
      ClientServer.instance().set_config(config)
    LOGGER.debug('The server sent the configuration to the client and released the lock.')

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
      # Fix for https://github.com/rec/echomesh/issues/342.
      data = Split.split_long_strings(base64.b64encode(self.bytes),
                                      _LONGEST_STRING)
      try:
        ClientServer.instance().write(type='light', data=data)
      except:
        self._fail()



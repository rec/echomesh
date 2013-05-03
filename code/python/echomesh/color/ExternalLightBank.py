from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy
import subprocess

from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.color import ColorTable
from echomesh.color import Client
from echomesh.color.LightBank import LightBank
from echomesh.expression import Units
from echomesh.network.Server import Server


_LONGEST_STRING = 3000

def _split_long_strings(s):
  result = []
  while len(s) > _LONGEST_STRING:
    result.append(s[0:_LONGEST_STRING])
    s = s[_LONGEST_STRING:]
  result.append(s)
  return result

class ExternalLightBank(LightBank):
  def __init__(self):
    self.process = None
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    config = Config.get('network', 'client')
    self.server = Server(config['host_name'], config['port'],
                         timeout=Units.convert(config['timeout']),
                         allow_reuse_address=config['allow_reuse_address'])
    self.server.start()

    if config['start']:
      self.process = subprocess.Popen(Client.make_command(),
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
    super(ExternalLightBank, self)._before_thread_start()

  def _send(self, **data):
    self.server.write(Yaml.encode_one(data), Yaml.SEPARATOR)

  def __del__(self):
    self.shutdown()

  def shutdown(self):
    with self.lock:
      if self.process:
        self._send(type='quit')
        self.process.terminate()

  def clear(self):
    with self.lock:
      self._send(type='clear')

  def config_update(self, get):
    super(ExternalLightBank, self).config_update(get)
    light = copy.deepcopy(get('light'))
    visualizer = light['visualizer']
    visualizer['background'] = ColorTable.to_color(visualizer['background'])

    dl = visualizer['instrument']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    with self.lock:
      self.server.set_config(Yaml.encode_one({'type': 'config', 'data': light}),
                             Yaml.SEPARATOR)

  def _after_thread_pause(self):
    super(ExternalLightBank, self)._after_thread_pause()
    self.shutdown()

  def _display_lights(self):
    with self.lock:
      self._send(type='light',
                 data=_split_long_strings(base64.b64encode(self.bytes)))

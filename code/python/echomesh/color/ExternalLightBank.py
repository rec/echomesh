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

class ExternalLightBank(LightBank):
  def __init__(self):
    self.client_type, cmd = Client.make_command()
    self.process = None
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    self.client_type, cmd = Client.make_command()
    if self.client_type == Client.ControlType.SOCKET:
      config = Config.get('network', 'client')

      self.server = Server(config['host_name'], config['port'],
                           timeout=Units.convert(config['timeout']),
                           allow_reuse_address=config['allow_reuse_address'])
      self.server.start()

    if Config.get('network', 'client', 'start'):
      self.process = subprocess.Popen(cmd,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
    else:
      assert self.client_type != Client.ControlType.TERMINAL
    super(ExternalLightBank, self)._before_thread_start()

  def _send(self, **data):
    yaml = Yaml.encode_one(data)

    if self.client_type == Client.ControlType.SOCKET:
      self.server.write(yaml)
      self.server.write(Yaml.SEPARATOR)
      self.server.flush()

    elif self.client_type == Client.ControlType.TERMINAL:
      if self.process:
        self.process.send_recv(s)
        self.process.send_recv(Yaml.SEPARATOR)
        self.process.flush()

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
    display = light['display']
    display['background'] = ColorTable.to_color(display['background'])

    dl = display['light']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    with self.lock:
      self._send(type='config', data=light)

  def _after_thread_pause(self):
    super(ExternalLightBank, self)._after_thread_pause()
    self.shutdown()

  def _send_compressed(self, lights, brightness):
    index = 0
    for i in xrange(self.count):
      light = i < len(lights) and lights[i]
      for j in xrange(3):
        if light:
          self.bytes[index] = ColorTable.denormalize(light[j], brightness)
        else:
          self.bytes[index] = 0

        index += 1
    debug_count = getattr(self, 'debug_count', 0)
    self._send(type='clight', data=str(self.bytes))

  def _display_lights(self, lights, brightness):
    with self.lock:
      self._send_compressed(lights, brightness)

  def _display_bytes(self):
    with self.lock:
      self._send(type='clight', data=base64.b64encode(self.bytes))

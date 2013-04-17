from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path
import subprocess

from echomesh.base import Config
from echomesh.base import Path
from echomesh.base import Yaml
from echomesh.color import ColorTable
from echomesh.color import Client
from echomesh.color.LightBank import LightBank
from echomesh.network.Server import Server
from echomesh.util import Log

LOGGER = Log.logger(__name__)

_QUIT = Yaml.encode_one({'type': 'quit'}) + Yaml.SEPARATOR

class ExternalLightBank(LightBank):
  def __init__(self):
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    super(ExternalLightBank, self)._before_thread_start()
    Config.add_client(self)

    self.client_type, cmd = Client.make_command()
    self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
    if self.client_type == Client.ControlType.SOCKET:
      self.server = Server(host, port, timeout)
      self.server.start()

  def _send_one(self, s):
    if self.client_type == Client.ControlType.SOCKET:
      self.server.send(s)
    elif self.client_type == Client.ControlType.TERMINAL:
      if self.process:
        self.process.send_recv(s)

  def _send(self, data_type, **data):
    result = {'type': data_type, 'data': data}
    self._send_one(Yaml.encode_one(result) + Yaml.SEPARATOR)

  def __del__(self):
    self.shutdown()

  def shutdown(self):
    with self.lock:
      if self.process:
        self.process.communicate(_QUIT)
        self.process = None

  def clear(self):
    with self.lock:
      self._send('clear')

  def config_update(self, get):
    light = copy.deepcopy(get('light'))
    display = light['display']
    display['background'] = ColorTable.to_color(display['background'])

    dl = display['light']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    with self.lock:
      self._send('config', **light)

  def _after_thread_pause(self):
    super(ExternalLightBank, self)._after_thread_pause()
    self.shutdown()

  def _display_lights(self, lights, brightness):
    with self.lock:
      self._send('light', colors=lights, brightness=brightness)



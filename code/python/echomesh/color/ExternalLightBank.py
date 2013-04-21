from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import subprocess

from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.color import ColorTable
from echomesh.color import Client
from echomesh.color.LightBank import LightBank
from echomesh.expression import Units
from echomesh.network.Server import Server
from echomesh.util import Log

LOGGER = Log.logger(__name__)

_QUIT = Yaml.encode_one({'type': 'quit'}) + Yaml.SEPARATOR

class ExternalLightBank(LightBank):
  def __init__(self):
    self.client_type, cmd = Client.make_command()
    self.process = None
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _before_thread_start(self):
    super(ExternalLightBank, self)._before_thread_start()
    self.client_type, cmd = Client.make_command()
    if self.client_type == Client.ControlType.SOCKET:
      config = Config.get('network', 'client')

      self.server = Server(config['host_name'], config['port'],
                           timeout=Units.convert(config['timeout']),
                           allow_reuse_address=config['allow_reuse_address'])
      self.server.start()

    if Config.get('network', 'client', 'start'):
      self.process = subprocess.Popen(cmd)
      #                                    stdin=subprocess.PIPE,
      #                                    stdout=subprocess.PIPE)
    else:
      assert self.client_type != Client.ControlType.TERMINAL

    Config.add_client(self)

  def _send_one(self, s):
    if self.client_type == Client.ControlType.SOCKET:
      self.server.write(s)
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
        self._send_one(_QUIT)
        self.process.terminate()

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

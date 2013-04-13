from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path
import subprocess

from echomesh.base import Config
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml
from echomesh.color import ColorTable
from echomesh.color.LightBank import LightBank
from echomesh.util import Log

LOGGER = Log.logger(__name__)

COMMAND = [os.path.join(Path.BINARY_PATH, 'echomesh')]

_QUIT = Yaml.encode_one({'type': 'quit'}) + Yaml.SEPARATOR

class ExternalLightBank(LightBank):
  def __init__(self):
    super(ExternalLightBank, self).__init__(is_daemon=True)

  def _send(self, data_type, **data):
    with self.lock:
      if self.process:
        result = {'type': data_type, 'data': data}
        output = Yaml.encode_one(result)
        self.display_count = getattr(self, 'display_count', 0) + 1
        if self.display_count < 4:
          print('!!!!!!!!\n', output)
        self.process.stdin.write(output)
        self.process.stdin.write(Yaml.SEPARATOR)
        self.process.stdin.flush()

  def __del__(self):
    self.shutdown()

  def shutdown(self):
    with self.lock:
      if self.process:
        self.process.communicate(_QUIT)
      self.process = None

  def clear(self):
    self._send('clear')

  def _before_thread_start(self):
    super(ExternalLightBank, self)._before_thread_start()
    cmd = (['sudo'] + COMMAND) if Platform.IS_LINUX else COMMAND
    self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    Config.add_client(self)

  def config_update(self, get):
    light = copy.deepcopy(get('light'))
    display = light['display']
    display['background'] = ColorTable.to_color(display['background'])

    dl = display['light']
    dl['border']['color'] = ColorTable.to_color(dl['border']['color'])
    dl['background'] = ColorTable.to_color(dl['background'])

    self._send('config', **light)

  def _after_thread_pause(self):
    super(ExternalLightBank, self)._after_thread_pause()
    self.shutdown()

  def _display_lights(self, lights, brightness):
    self._send('light', colors=lights, brightness=brightness)


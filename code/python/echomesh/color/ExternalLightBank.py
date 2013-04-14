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
    if self.process:
      result = {'type': data_type, 'data': data}
      output = Yaml.encode_one(result)
      debug = data_type == 'light'
      if debug: print('!!!! 1')
      self.process.stdin.write(output)
      self.process.stdin.flush()
      if debug: print('!!!! 2')
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
    with self.lock:
      self._send('clear')

  def _before_thread_start(self):
    super(ExternalLightBank, self)._before_thread_start()
    cmd = (['sudo'] + COMMAND) if Platform.IS_LINUX else COMMAND
    self.process = subprocess.Popen(cmd,
                                    stdin=subprocess.PIPE)
      #                                    stdout=subprocess.PIPE,
      #                                   stderr=subprocess.PIPE)
    Config.add_client(self)

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


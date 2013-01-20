from __future__ import absolute_import, division, print_function, unicode_literals

import time
import traceback

from echomesh.base import Config
from echomesh.sound import Input
from echomesh.sound import Levels
from echomesh.util import Log
from echomesh.base import Platform
from echomesh.util.math import Average
from echomesh.util.thread import Openable
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048

class Microphone(ThreadLoop.ThreadLoop):
  def __init__(self, callback):
    super(Microphone, self).__init__(name='Microphone')
    self.set_config()
    self.callback = callback
    self.previous_level_name = None
    self.errors = 0

  def reset_levels(self):
    self.level = -100.0
    self.max_level = self.level
    self.min_level = 0.0

  def run(self):
    average = Average.average(
      self._get_next_level(),
      moving_window=Config.get('audio', 'input', 'average', 'window_size'),
      grouped_window=Config.get('audio', 'input', 'average', 'group_size'))

    for level in average:
      if not self.is_open:
        return
      if Config.get('audio', 'input', 'verbose'):
        LOGGER.info('%s: %.2f', self.levels.name(level), level)

      level_name = self.levels.name(level)
      if level_name != self.previous_level_name:
        self.callback(level_name)
        self.previous_level_name = level_name

  def start(self):
    self.reset_levels()
    LOGGER.info('Microphone starting')
    rate = Config.get('audio', 'input', 'sample_rate')
    use_default = Config.get('audio', 'input', 'use_default_channel')
    sample_bytes = Config.get('audio', 'input', 'sample_bytes')
    self.stream = Input.get_pyaudio_stream(rate, use_default, sample_bytes)

    if getattr(self, 'stream', None):
      super(Microphone, self).start()
    else:
      self.close()

  def set_config(self):
    self.levels = Levels.Levels(**Config.get('audio', 'input', 'levels'))
    chunk_size = Config.get('audio', 'input', 'average', 'chunk_size')
    self.chunk_size = min(max(chunk_size, MIN_CHUNK_SIZE), MAX_CHUNK_SIZE)

  def _get_next_level(self):
    while self.is_open:
      try:
        self.level = Input.get_mic_level(self.stream.read(self.chunk_size))
        self.max_level = max(self.level, self.max_level)
        self.min_level = min(self.level, self.min_level)
        yield self.level
      except GeneratorExit:
        pass
      except IOError:
        self.errors += 1
        if not (self.errors % 20):
          LOGGER.error('errors %d', self.errors)

      except:
        LOGGER.critical(traceback.format_exc())


def microphone(callback):
  if Config.get('audio', 'input', 'enable'):
    return Microphone(callback)
  else:
    LOGGER.info('Mic thread disabled')


from __future__ import absolute_import, division, print_function, unicode_literals

import time
import traceback

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.sound import Input
from echomesh.sound import Levels
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util.math import Average
from echomesh.util.thread import RunnableThread

LOGGER = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048

class Microphone(RunnableThread.RunnableThread):
  COMPARE_ATTRIBUTES = 'index', 'name', 'rate', 'sample_bytes'

  def __init__(self, callback):
    super(Microphone, self).__init__(name='Microphone')
    self.callback = callback
    self.previous_level_name = None
    self.errors = 0
    Config.add_client(self)

  def config_update(self, get):
    def state():
      return [getattr(self, a, 0) for a in Microphone.COMPARE_ATTRIBUTES]
    old = state()
    chunk_size = get('audio', 'input', 'average', 'chunk_size')
    self.chunk_size = min(max(chunk_size, MIN_CHUNK_SIZE), MAX_CHUNK_SIZE)
    self.grouped_window = get('audio', 'input', 'average', 'group_size')
    self.index = Sound.get_input_index(get)
    self.levels = Levels.Levels(**get('audio', 'input', 'levels'))
    self.moving_window = get('audio', 'input', 'average', 'window_size')
    self.name = get('audio', 'input', 'name')
    self.rate = get('audio', 'input', 'sample_rate')
    self.sample_bytes = get('audio', 'input', 'sample_bytes')
    self.verbose = get('audio', 'input', 'verbose')
    if self.is_running and state() != old:
      # TODO: restart the py_audio_stream.
      pass

  def reset_levels(self):
    self.level = -100.0
    self.max_level = self.level
    self.min_level = 0.0

  def target(self):
    average = Average.average(
      self._get_next_level(),
      moving_window=self.moving_window,
      grouped_window=self.grouped_window)

    for level in average:
      if not self.is_running:
        return
      if self.verbose:
        LOGGER.info('%s: %.2f', self.levels.name(level), level)

      level_name = self.levels.name(level)
      if level_name != self.previous_level_name:
        self.callback(level_name)
        self.previous_level_name = level_name

  def start(self):
    self.reset_levels()
    LOGGER.info('Microphone starting')
    self.stream = Input.get_pyaudio_stream(self.name, self.index, self.rate,
                                           self.sample_bytes)

    if getattr(self, 'stream', None):
      super(Microphone, self).start()
    else:
      self.stop()

  def _get_next_level(self):
    while self.is_running:
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


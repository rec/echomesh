from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.sound import Input
from echomesh.sound import Levels
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util.math import Average
from echomesh.util.thread import ThreadRunnable

LOGGER = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048

class Microphone(ThreadRunnable.ThreadRunnable):
  COMPARE_ATTRIBUTES = 'device_index', 'device_name', 'rate', 'sample_bytes'

  def __init__(self, callback):
    super(Microphone, self).__init__(name='Microphone')
    self.callback = callback
    self.previous_level_name = None
    self.stream = None
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
    self.device_name = get('audio', 'input', 'device_name')
    self.rates = get('audio', 'input', 'sample_rate')
    try:
      len(self.rates)
    except TypeError:
      self.rates = [self.rates]
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

  def _before_thread_start(self):
    try:
      self.reset_levels()
      self.stream = Input.get_pyaudio_stream(
        self.device_name, self.index, self.rates, self.sample_bytes)
    except:
      LOGGER.error('Microphone error for %s, %s', self.device_name, self.index,
                   exc_info=1)
    else:
      if not self.stream:
        LOGGER.error('Failed to open stream %s, %s', self.device_name,
                     self.index)
        self.pause()
      else:
        LOGGER.debug('Microphone started.')

  def _get_next_level(self):
    while self.is_running:
      try:
        self.level = Input.get_mic_level(self.stream.read(self.chunk_size))
        self.max_level = max(self.level, self.max_level)
        self.min_level = min(self.level, self.min_level)
        yield self.level
      except GeneratorExit:
        pass
      except:
        if self.is_running:
          LOGGER.error(limit=20, every=20)


def microphone(callback):
  if Config.get('audio', 'input', 'enable'):
    try:
      return Microphone(callback)
    except Exception:
      LOGGER.error('Failed to turn on mic.')
  else:
    LOGGER.info('Mic thread disabled')


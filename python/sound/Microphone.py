from __future__ import absolute_import, division, print_function, unicode_literals

import traceback

from config import Config
from sound import Levels
from util import Average
from util import Log
from util import Openable
from util import Platform
from util import ThreadLoop
from util import Util

LOGGER = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_SAMPLE_RATE = 8000
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048
MAX_INPUT_DEVICES = 6

# TODO: a better way to identify that stream.
def get_pyaudio_stream(rate, use_default=False):
  import pyaudio

  pyaud = pyaudio.PyAudio()

  def _make_stream(i):
    stream = pyaud.open(format=pyaudio.paInt16, channels=1, rate=rate,
                        input_device_index=i, input=True)
    LOGGER.info('Opened pyaudio stream %d', i)
    return stream
    # TODO: move format into config.

  if use_default:
    index = pyaud.get_default_input_device_info()['index']
    print("Trying to open", index)
    return _make_stream(index)
  else:
    for i in range(MAX_INPUT_DEVICES):
      try:
        stream = _make_stream(i)
        return stream
      except:
        pass

  LOGGER.error("Couldn't create pyaudio input stream %d", rate)

def call_if_different(callback, initial=None):
  old_val = [initial]
  def cb(value):
    if value != old_val[0]:
      old_val[0] = value
      callback(value)
  return cb

def get_mic_level(data, length=-1, dtype=None):
  import analyse
  import numpy

  if dtype is None:
    dtype = numpy.int16

  samps = numpy.fromstring(data, dtype=dtype, count=length)
  return analyse.loudness(samps)

class Microphone(ThreadLoop.ThreadLoop):
  def __init__(self, config, callback):
    ThreadLoop.ThreadLoop.__init__(self)
    self.set_config(config)
    self.callback = callback
    self.previous_level = None

  def run(self):
    def get_next_level():
      while self.is_open:
        try:
          yield get_mic_level(self.stream.read(self.chunksize))
        except:
          LOGGER.critical(traceback.format_exc())

    average = Average.average(
      get_next_level(),
      moving_window=self.aconfig.get('moving_window', 0),
      grouped_window=self.aconfig.get('grouped_window', 0))
    for level in average:
      if self.aconfig.get('verbose', False):
        LOGGER.info('%s: %.2f', self.levels.name(level), level)
      level_name = self.levels.name(level)
      if level_name != self.previous_level:
        self.callback(level_name)
        self.previous_level = level_name

  def start(self):
    if Config.is_enabled('audio', 'input'):
      rate = self.aconfig.get('samplerate', DEFAULT_SAMPLE_RATE)
      use_default = self.aconfig.get('use_default', False)
      LOGGER.info('Starting pyaudio')
      self.stream = get_pyaudio_stream(rate, use_default)

    if getattr(self, 'stream', None):
      ThreadLoop.ThreadLoop.start(self)
    else:
      self.close()

  def set_config(self, config):
    self.config = config
    self.aconfig = config['audio']['input']
    self.library = config['audio']['library']
    self.levels = Levels.Levels(**self.aconfig['levels'])
    self.chunksize = min(max(self.aconfig.get('chunksize', DEFAULT_CHUNK_SIZE),
                             MIN_CHUNK_SIZE), MAX_CHUNK_SIZE)


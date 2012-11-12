from __future__ import absolute_import, division, print_function, unicode_literals

import time
import traceback

from config import Config
from sound import Levels
from util import Average
from util import Log
from util import Openable
from util import Platform
from util.ThreadLoop import ThreadLoop
from util import Util

LOGGER = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_SAMPLE_RATE = 4000
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048
MAX_INPUT_DEVICES = 6
DEFAULT_SAMPLE_BYTES = 2

# TODO: a better way to identify that stream.
def get_pyaudio_stream(rate, use_default, sample_bytes):
  import pyaudio

  pyaud = pyaudio.PyAudio()
  FORMAT_NAMES = {1: pyaudio.paInt8, 2: pyaudio.paInt16, 3:
                  pyaudio.paInt24, 4: pyaudio.paInt32}
  format = FORMAT_NAMES.get(sample_bytes, 0)
  if not format:
    LOGGER.error("Didn't understand sample_bytes=%s", sample_bytes)
    format = FORMAT_NAMES[1]

  def _make_stream(i):
    stream = pyaud.open(format=format, channels=1, rate=rate,
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

def get_mic_level(data, length=-1, dtype=None):
  import analyse
  import numpy

  if dtype is None:
    dtype = numpy.int16

  samps = numpy.fromstring(data, dtype=dtype, count=length)
  return analyse.loudness(samps)

class Microphone(ThreadLoop):
  def __init__(self, config, callback):
    super(Microphone, self).__init__()
    self.set_config(config)
    self.callback = callback
    self.previous_level = None
    self.errors = 0

  def run(self):
    def get_next_level():
      while self.is_open:
        try:
          yield get_mic_level(self.stream.read(self.chunksize))
          print('!!!')
        except IOError:
          if False:
            if self.errors > 2000:
              self.close()
              LOGGER.error('Too many errors, closed')
            if not (self.errors % 20):
              time.sleep(20)
              LOGGER.debug('More errors ')
          self.errors += 1
        except:
          LOGGER.critical(traceback.format_exc())

    average = Average.average(
      get_next_level(),
      moving_window=self.aconfig.get('moving_window', 0),
      grouped_window=self.aconfig.get('grouped_window', 0))
    for level in average:
      if not self.is_open:
        return

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
      sample_bytes = self.aconfig.get('sample_bytes', DEFAULT_SAMPLE_BYTES)
      LOGGER.info('Starting pyaudio')
      self.stream = get_pyaudio_stream(rate, use_default, sample_bytes)

    if getattr(self, 'stream', None):
      super(Microphone, self).start()
    else:
      self.close()

  def set_config(self, config):
    self.config = config
    self.aconfig = config['audio']['input']
    self.levels = Levels.Levels(**self.aconfig['levels'])
    self.chunksize = min(max(self.aconfig.get('chunksize', DEFAULT_CHUNK_SIZE),
                             MIN_CHUNK_SIZE), MAX_CHUNK_SIZE)


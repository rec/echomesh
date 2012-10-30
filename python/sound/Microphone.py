from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Average
from util import Log
from util import Openable
from util import Platform
from util import ThreadLoop
from util import Util

from sound import Levels

LOGGING = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_SAMPLE_RATE = 8000
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048
MAX_INPUT_DEVICES = 64

# TODO: a better way to identify that stream.
def get_pyaudio_stream(rate, use_default=False):
  import pyaudio

  pyaud = pyaudio.PyAudio()

  def _make_stream(i):
    stream = pyaud.open(format=pyaudio.paInt16, channels=1, rate=rate,
                        input_device_index=i, input=True)
    LOGGING.info('Opened pyaudio stream %d', i)
    return stream
    # TODO: move format into config.

  if use_default:
    index = pyaud.get_default_input_device_info()['index']
    return _make_stream(index)
  else:
    for i in range(MAX_INPUT_DEVICES):
      try:
        return _make_stream(i)
      except:
        pass

  LOGGING.error("Coudn't create pyaudio input stream %d", rate)

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
    average = Average.average(
      callback,
      moving_window=self.aconfig.get('moving_window', 0),
      grouped_window=self.aconfig.get('grouped_window', 0))
    self.callback = Util.call_if_different(average)

  def start(self):
    if Config.is_enabled(self.config, 'audio', 'input'):
      rate = self.aconfig.get('samplerate', DEFAULT_SAMPLE_RATE)
      use_default = self.aconfig.get('use_default', False)
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

  def run(self):
    level = get_mic_level(self.stream.read(self.chunksize))
    if self.aconfig.get('verbose', False):
      LOGGER.info('%s: %.2f', self.levels.name(level), level)
    self.callback(self.levels.name(level))

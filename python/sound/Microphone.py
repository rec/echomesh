from __future__ import absolute_import, division, print_function, unicode_literals

import analyse
import numpy
import pyaudio

from util import Log
from util import Openable
from util import Platform
from util import ThreadLoop
from util import Util

LOGGING = Log.logger(__name__)

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_SAMPLE_RATE = 8000
DEFAULT_PERIOD_SIZE = 160
DEFAULT_CHUNK_SIZE = 1024
MAX_INPUT_DEVICES = 64

def mic_input_alsa(config, rate):
  import alsaaudio

  conf = config['audio']['input']
  name = conf['name']
  card = conf.get('card', DEFAULT_CARD_FORMAT % name)
  stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
  stream.setchannels(1)
  stream.setrate(rate)

  if 'periodsize' in conf:
    stream.setperiodsize(conf['periodsize'])

  return lambda: stream.read()

def _make_stream(pyaud, rate, index):
  return pyaud.open(
    format=pyaudio.paInt16,  # TODO: move this into config.
    channels=1,
    rate=rate,
    input_device_index=index,
    input=True)


# TODO: a better way to identify that stream.
def _get_pyaudio_stream(pyaud, rate, use_default=False):
  if use_default:
    index = pyaud.get_default_input_device_info()['index']
    return _make_stream(pyaud, rate, index)
  else:
    for i in range(MAX_INPUT_DEVICES):
      try:
        return _make_stream(pyaud, rate, i)
      except:
        pass

  LOGGING.error("Coudn't create pyaudio input stream %d", rate)

def mic_input_pyaudio(config, rate):
  pyaud = pyaudio.PyAudio()
  stream = _get_pyaudio_stream(pyaud, rate)
  if stream:
    chunksize = config['audio']['input'].get('chunksize', DEFAULT_CHUNK_SIZE)
    return lambda: (-1, stream.read(chunksize))

def get_input_stream(config):
  conf = config['audio']

  if conf['input'].get('enable', True):
    rate = conf['input'].get('samplerate', DEFAULT_SAMPLE_RATE)
    library = conf['library']
    if library == 'pyaudio':
      return mic_input_pyaudio(config, rate)
    elif library == 'alsaaudio':
      return mic_input_alsa(config, rate)
    else:
      LOGGING.error("Don't understand audio library '%s'", library)

def get_mic_level(length, data):
  samps = numpy.fromstring(data, dtype=numpy.int16, count=length)
  return analyse.loudness(samps)

def run_mic_levels_thread(callback, config):
  stream = get_input_stream(config)

  if not stream:
    return Openable.Openable()

  cb_different = Util.call_if_different(callback)
  def cb():
    level = get_mic_level(*stream())
    slot = Util.level_slot(level, config['audio']['input']['levels'])
    cb_different(slot)

  return ThreadLoop.ThreadLoop(cb)

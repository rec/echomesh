from __future__ import absolute_import, division, print_function, unicode_literals

import analyse
import numpy

from util import Openable
from util import Platform
from util import ThreadLoop
from util import Util

DEFAULT_CARD_FORMAT = 'sysdefault:CARD=%s'
DEFAULT_SAMPLE_RATE = 8000
DEFAULT_PERIOD_SIZE = 160

def mic_input_linux(config):
  import alsaaudio

  conf = config['mic']
  name = conf['name']
  card = conf.get('card', DEFAULT_CARD_FORMAT % name)
  mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
  mic.setchannels(1)
  if 'samplerate' in conf:
    mic.setrate(conf['samplerate'])

  if 'periodsize' in conf:
    mic.setperiodsize(conf['periodsize'])

  return lambda: mic.read()

def mic_input_mac(config):
  if True:
    return Openable.Openable()

  import pyaudio

  pa = pyaudio.PyAudio()
  conf = config['mic']
  name = conf['name']

  for i in range(pa.get_device_count()):
    devinfo = pa.get_device_info_by_index(i)
    # print('"%s" "%s"' % (devinfo['name'], name))
    if devinfo['name'].strip() == name:
      index = i
      break
  else:
    return Openable.Openable()

  frames = conf.get('periodsize', DEFAULT_PERIOD_SIZE)
  str = pa.open(format=pyaudio.paInt16,
                channels=1,
                rate=conf.get('samplerate', DEFAULT_SAMPLE_RATE),
                input=True,
                input_device_index=index,
                frames_per_buffer=frames)
  def cb():
    print('here')
    block = self.stream.read(frames)
    print(block)
    return len(block), block

  return cb

def get_mic_level(mic):
  length, data = mic()
  samps = numpy.fromstring(data, dtype=numpy.int16, count=length)
  return analyse.loudness(samps)

def run_mic_levels_thread(callback, config):
  if  not config['mic'].get('enable', True):
    return Openable.Openable()

  mic = mic_input_linux(config) if Platform.IS_LINUX else mic_input_mac(config)
  cb_different = Util.call_if_different(callback)
  def cb():
    level = get_mic_level(mic)
    slot = Util.level_slot(level, config['mic']['levels'])
    cb_different(slot)

  return ThreadLoop.ThreadLoop(cb)

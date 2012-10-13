from __future__ import absolute_import, division, print_function, unicode_literals

import alsaaudio
import analyse
import numpy

DEFAULT_CARD = 'sysdefault:CARD=AK5370'

def mic_input(config):
  card = config.mic.get('card', DEFAULT_CARD)
  mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
  mic.setchannels(1)
  if 'samplerate' in config.mic:
    mic.setrate(config.mic['samplerate'])

  if 'periodsize' in config.mic:
    mic.setperiodsize(config.mic['periodsize'])

  return mic

def get_mic_level(mic):
  length, data = mic.read()
  samps = numpy.fromstring(data, dtype=numpy.int16, count=length)
  return analyse.loudness(samps)

def run_mic_thread(mic, callback):
  thread = threading.Thread(target=lambda: callback(get_mic_level(mic)))
  thread.start()

  return thread

def level_slot(level, levels):
  for i, lev in enumerate(levels):
    if level < lev:
      return i
  return len(levels)

def call_if_different(callback, initial=None):
  def cb(value):
    if value != initial:
      initial = value
      callback(value)
  return cb

def run_mic_levels_thread(mic, callback, config):
  levels = config.mic['levels'] + [10000]
  assert len(callbacks) is len(levels)
  def cb(level):
    for i, lev in enumerate(levels):
      if level < lev:
        return callback(i)

  return run_mic_thread(mic, cb)

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

MAX_INPUT_DEVICES = 6
TRY_ALL_DEVICES = False

# TODO: a better way to identify that stream.
def get_pyaudio_stream(name, index, rate, sample_bytes):
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

    LOGGER.info('Opened pyaudio stream %s',
                pyaud.get_device_info_by_index(i)['name'])
    return stream

  if TRY_ALL_DEVICES:
  # Consider removing this.
    for i in range(MAX_INPUT_DEVICES):
      try:
        stream = _make_stream(i)
        return stream
      except:
        pass

  if index is None:
    if name:
      for i in range(pyaudio.get_device_count()):
        if pyaud.get_device_info_by_index(i)['name'].startswith(name):
          index = i
          break
      else:
        LOGGER.error("Didn't find audio input device named %s", name)

    if index is None:
      index = pyaud.get_default_input_device_info()['index']
  return _make_stream(index)


  else:
  LOGGER.error("Couldn't create pyaudio input stream %d", rate)

def get_mic_level(data, length=-1, dtype=None):
  import analyse
  import numpy

  if dtype is None:
    dtype = numpy.int16

  samps = numpy.fromstring(data, dtype=dtype, count=length)
  return analyse.loudness(samps)

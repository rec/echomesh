from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import os.path
import sndhdr
import sunau
import wave

from sound import Sound
from util import ThreadLoop

DEFAULT_CHUNK_SIZE = 1024
BITS_PER_BYTE = 8

class FilePlayer(ThreadLoop.ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)

  def __init__(self, filename, chunk_size=DEFAULT_CHUNK_SIZE):
    ThreadLoop.ThreadLoop.__init__(self)

    self.debug = True
    self.chunk_size = chunk_size

    fname = os.path.expanduser(filename)
    (type, sampling_rate, self.channels,
     frames, bits_per_sample) = sndhdr.what(fname)

    self.file_stream = FilePlayer.HANDLERS[type].open(filename, 'rb')
    format = Sound.PYAUDIO.get_format_from_width(bits_per_sample / BITS_PER_BYTE)
    self.stream = Sound.PYAUDIO.open(format=format,
                                     channels=self.channels,
                                     rate=sampling_rate,
                                     output=True)

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
    self.stream.stop_stream()
    self.stream.close()

  def run(self):
    data = self.file_stream.readframes(self.chunk_size)
    if data:
      self.stream.write(data)
    else:
      self.close()


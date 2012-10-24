from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import numpy
import os.path
import sndhdr
import struct
import sunau
import wave

from sound import Sound
from util import ThreadLoop

DEFAULT_CHUNK_SIZE = 1024
BITS_PER_BYTE = 8

class FilePlayer(ThreadLoop.ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)

  def __init__(self, filename, level=None, pan=None,
               chunk_size=DEFAULT_CHUNK_SIZE):
    ThreadLoop.ThreadLoop.__init__(self)

    self.debug = True
    self.chunk_size = chunk_size
    self.level = level
    self.pan = pan

    fname = os.path.expanduser(filename)
    filetype = sndhdr.what(fname)[0]
    self.file_stream = FilePlayer.HANDLERS[filetype].open(filename, 'rb')
    self.sample_width = self.file_stream.getsampwidth()
    format = Sound.PYAUDIO.get_format_from_width(self.sample_width)

    (self.channels, self.sample_width, self.sampling_rate,
     n, c1, c2) = self.file_stream.getparams()
    channels = 2 if self.pan else self.channels
    self.audio_stream = Sound.PYAUDIO.open(format=format,
                                           channels=channels,
                                           rate=self.sampling_rate,
                                           output=True)

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
    self.audio_stream.stop_stream()
    self.audio_stream.close()

  def run(self):
    data = self.file_stream.readframes(self.chunk_size)
    if data:
      if self.pan or self.level:
        frames = numpy.fromstring(data, dtype=self.dtype)
        for i, s in enumerate(frames):
          frames[i] = self.level * s
        data = numpy.frombuffer(frames, dtype=self.dtype)

      self.audio_stream.write(data)
    else:
      self.close()


# from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import numpy
import os.path
import sndhdr
import struct
import sunau
import wave

from sound import Sound
from util import ThreadLoop

# DEFAULT_CHUNK_SIZE = 1024
DEFAULT_CHUNK_SIZE = 8
BITS_PER_BYTE = 8
DEBUG = False

def _print_string(frames):
  if not DEBUG:
    return

  print('  *****')
  print('_print_string', len(frames), type(frames))
  for f in frames:
    print(ord(f))
  print('  *****')

def _print_frame(frames):
  if not DEBUG:
    return

  print('  *****')
  print('_print_frame', len(frames), type(frames))
  for f in frames:
    print(f)
  print('  *****')

def uninterleave(src):
  """Convert one stereo source into two mono sources."""
  return src.reshape(2, len(src)/2, order='FORTRAN')


class FilePlayer(ThreadLoop.ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)
  DTYPES = {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

  def __init__(self, filename, level=-1.0, pan=None,
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
    self.dtype = FilePlayer.DTYPES[self.sample_width]
    self.request_channels = 2 if self.pan else self.channels
    self.audio_stream = Sound.PYAUDIO.open(format=format,
                                           channels=self.request_channels,
                                           rate=self.sampling_rate,
                                           output=True)

    self.must_convert = ()

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
    self.audio_stream.stop_stream()
    self.audio_stream.close()

  def _convert(self, frames):
    frames = numpy.fromstring(frames, dtype=self.dtype)
    if self.sample_width is 1:
      frames *= 256.0
    elif self.sample_width is 4:
      frames /= 65536.0

    if True:
      return frames

    if self.channels is 1:
      return numpy.vstack((frames, frames))
    else:
      return uninterleave(frames)

  def run(self):
    frames = self.file_stream.readframes(self.chunk_size)
    if frames:
      if self.pan or self.level >= 0.0:
        new_frames = self._convert(frames)
        new_frames *= self.level
        frames = new_frames.tostring()

      self.audio_stream.write(frames)
    else:
      self.close()


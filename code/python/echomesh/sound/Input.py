from __future__ import absolute_import, division, print_function, unicode_literals

class Input(object):
  def __init__(self, dtype=None):
    import numpy

    self.frames = self.numpy_frames = self.level = None
    self.dtype = numpy.int16 if dtype is None else dtype

  def receive(self, frames):
    import numpy

    self.frames = frames
    self.numpy_frames = numpy.fromstring(frames, dtype=self.dtype, count=-1)

    import analyse
    self.level = analyse.loudness(self.numpy_frames)

cdef extern from "echomesh/audio/Loudness.h" namespace "echomesh::audio":
  cdef cppclass Loudness:
    float loudness()
  Loudness* loudnessInput(string name, int channels, int windowSize)

cdef class AudioLoudness:
  cdef Loudness* thisptr

  def __cinit__(self, string name, int channels, int windowSize = 1024):
    self.thisptr = loudnessInput(name, channels, windowSize)
    if not self.thisptr:
      raise Exception('Couldn\'t create input for %s:%d' % (name, channels))

  def __dealloc__(self):
    del self.thisptr

  def loudness(self):
    return self.thisptr.loudness()



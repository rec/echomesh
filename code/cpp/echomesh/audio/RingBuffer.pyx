# Really just for testing.

cdef extern from "JuceLibraryCode/modules/juce_audio_basics/buffers/juce_AudioSampleBuffer.h" namespace "juce":
  cdef cppclass AudioSampleBuffer:
    AudioSampleBuffer(int channels, int size)
    float* getSampleData(int channel)

cdef extern from "echomesh/audio/RingBuffer.h" namespace "echomesh::audio":
  cdef cppclass RingBuffer:
    RingBuffer(int channels, int size)
    bool write(AudioSampleBuffer)
    bool read(AudioSampleBuffer*)
    int sampleCount()
    int size()
    int channels()

cdef class AudioRingBuffer:
  cdef RingBuffer* thisptr

  def __cinit__(self, int channels, int size):
    self.thisptr = new RingBuffer(channels, size)

  def __dealloc__(self):
    del self.thisptr

  def sample_count(self):
    return self.thisptr.sampleCount()

  def read(self, int size, list data):
    cdef int channels = self.thisptr.channels()
    cdef AudioSampleBuffer* buffer
    cdef float* channel_data
    buffer = new AudioSampleBuffer(channels, size)
    try:
      success = self.thisptr.read(buffer)
      for channel in range(channels):
        channel_data = buffer.getSampleData(channel)
        data.append([channel_data[j] for j in range(size)])

      return success
    finally:
      del buffer

  def write(self, data):
    cdef int channels = len(data)
    cdef int size = len(data[0])
    cdef AudioSampleBuffer* buffer
    cdef float* channel_data
    assert channels == self.thisptr.channels()

    buffer = new AudioSampleBuffer(channels, size)
    try:
      for channel, cdata in enumerate(data):
        assert len(cdata) == size
        channel_data = buffer.getSampleData(channel)
        for sample_index, data_point in enumerate(cdata):
          channel_data[sample_index] = data_point
      return self.thisptr.write(buffer[0])
    finally:
      del buffer

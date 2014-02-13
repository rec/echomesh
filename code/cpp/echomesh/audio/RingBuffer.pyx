# Really just for testing.

cdef extern from "JuceLibraryCode/modules/juce_audio_basics/buffers/juce_AudioSampleBuffer.h" namespace "juce":
  cdef cppclass AudioSampleBuffer:
    AudioSampleBuffer()
    void setSize(int channels, int size)
    float* getSampleData(int channel, int offset)

cdef extern from "echomesh/audio/RingBuffer.h" namespace "echomesh::audio":
  cdef cppclass RingBuffer:
    RingBuffer(int channels, int size)
    void append(AudioSampleBuffer)
    void fill(AudioSampleBuffer*)
    int sampleCount()

cdef class AudioRingBuffer:
  cdef RingBuffer* thisptr

  def __cinit__(self, int channels, int size):
    self.thisptr = new RingBuffer(channels, size)

  def __dealloc__(self):
    del self.thisptr



cdef extern from "echomesh/audio/Loudness.h" namespace "echomesh::audio":
    cdef cppclass Loudness:
        float loudness()
    Loudness* loudnessInput(
      string name, int channels, int chunkSize, int sampleRate)

cdef class AudioLoudness:
    cdef Loudness* thisptr

    def __cinit__(self, string name='', int channels=1, int
                  chunk_size=1024, int sample_rate=0):
        self.thisptr = loudnessInput(name, channels, chunk_size, sample_rate)
        if not self.thisptr:
            raise Exception('Couldn\'t create input for %s:%d' % (name, channels))

    def __dealloc__(self):
        del self.thisptr

    def loudness(self):
        return self.thisptr.loudness()

#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class RingBuffer {
 public:
  RingBuffer(int channels, int size);
  bool write(int count, const float** samples);
  bool write(const AudioSampleBuffer&);

  bool read(const AudioSourceChannelInfo& info);
  bool read(AudioSampleBuffer*);

  int sampleCount() const;
  int size() const { return size_; }
  int channels() const { return channels_; }

 private:
  AudioSampleBuffer buffer_;
  int begin_, end_, overruns_, underruns_;
  const int channels_;
  const int size_;
  bool lastOperationWasWrite_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(RingBuffer);
};

}  // namespace audio
}  // namespace echomesh

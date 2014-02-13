#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class RingBuffer {
 public:
  RingBuffer(int channels, int size);
  ~RingBuffer();

  bool write(int count, const float** samples);
  bool write(const AudioSampleBuffer&);

  bool read(const AudioSourceChannelInfo& info);
  bool read(AudioSampleBuffer*);

  int available() const;
  int size() const;
  int channels() const { return channels_; }

 private:
  class Index;

  unique_ptr<Index> index_;
  AudioSampleBuffer buffer_;
  const int channels_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(RingBuffer);
};

}  // namespace audio
}  // namespace echomesh

#include "echomesh/audio/RingBuffer.h"

namespace echomesh {
namespace audio {

RingBuffer::RingBuffer(int channels, int size)
    : buffer_(channels, size), begin_(0), end_(0), overruns_(0), underruns_(0),
      channels_(channels), size_(size) {
}

void RingBuffer::append(int count, const float** samples) {
  bool twoParts;
  int oldEnd, newEnd;
  {
    ScopedLock l(lock_);
    auto forward = (begin_ <= end_);
    oldEnd = end_;

    end_ += count;
    twoParts = (end_ > size_);
    if (twoParts)
      end_ -= size_;
    newEnd = end_;

    if (forward == twoParts and begin_ <= end_) {
      overruns_ += 1;
      begin_ = end_ + 1;
      if (begin_ >= size_)
        begin_ -= size_;
    }
  }

  if (twoParts) {
    auto first = size_ - oldEnd;
    auto second = count - first;
    for (auto i = 0; i < channels_; ++i) {
      buffer_.copyFrom(i, oldEnd, samples[i], first);
      buffer_.copyFrom(i, 0, samples[i] + first, second);
    }
  } else {
    for (auto i = 0; i < channels_; ++i)
      buffer_.copyFrom(i, oldEnd, samples[i], count);
  }
}

void RingBuffer::remove(AudioSampleBuffer* buffer) {
  // auto bufferSize = buffer->getNumSamples();

}

}  // namespace audio
}  // namespace echomesh

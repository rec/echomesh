#include "echomesh/audio/RingBuffer.h"

namespace echomesh {
namespace audio {

RingBuffer::RingBuffer(int channels, int size)
    : buffer_(channels, size), begin_(0), end_(0), overruns_(0), underruns_(0),
      channels_(channels), size_(size) {
}

void RingBuffer::appendFrom(int count, const float** samples) {
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

void RingBuffer::appendFrom(const AudioSampleBuffer& buffer) {
  appendFrom(buffer.getNumSamples(),
             const_cast<const float**>(buffer.getArrayOfChannels()));
}

void RingBuffer::fill(const AudioSourceChannelInfo& info) {
  auto count = info.numSamples;
  bool twoParts;
  int oldBegin, newBegin;
  {
    ScopedLock l(lock_);
    oldBegin = begin_;
    auto forward = (begin_ <= end_);
    auto remaining = end_ - begin_;
    if (not forward)
      remaining += size_;
    if (count > remaining) {
      underruns_ += 1;
      count = remaining;
    }

    auto firstPart = (forward ? end_ : size_) - oldBegin;
    twoParts = firstPart < count;
    if (twoParts)
      begin_ = count - firstPart;
    else
      begin_ = begin_ + count;
    newBegin = begin_;
  }

  if (twoParts) {
    auto first = size_ - oldBegin;
    auto second = count - first;
    for (auto i = 0; i < channels_; ++i) {
      info.buffer->copyFrom(i, info.startSample, buffer_, i, oldBegin, first);
      info.buffer->copyFrom(i, info.startSample + first, buffer_, i, 0, second);
    }
  } else {
    for (auto i = 0; i < channels_; ++i)
      info.buffer->copyFrom(i, info.startSample, buffer_, i, oldBegin, count);
  }
}

void RingBuffer::fill(AudioSampleBuffer* buffer) {
  fill(AudioSourceChannelInfo(buffer, 0, buffer->getNumSamples()));
}

int RingBuffer::sampleCount() const {
  ScopedLock l(lock_);
  auto result = end_ - begin_;
  if (result < 0)
    result += size_;
  return result;
}

}  // namespace audio
}  // namespace echomesh

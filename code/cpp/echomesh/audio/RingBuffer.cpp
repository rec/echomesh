#include "echomesh/audio/RingBuffer.h"
#include "echomesh/audio/RingBufferIndex.h"

namespace echomesh {
namespace audio {

class RingBuffer::Index : public RingBufferIndex<int> {
 public:
  explicit Index(int size) : RingBufferIndex<int>(size) {}
};

RingBuffer::RingBuffer(int channels, int size)
    : index_(new Index(size)), buffer_(channels, size), channels_(channels) {
}

RingBuffer::~RingBuffer() {}

bool RingBuffer::write(int count, const float** samples) {
  auto blocks = index_->write(count);
  auto total = 0;
  for (auto& b: blocks) {
    auto size = b.second - b.first;
    for (auto c = 0; c < channels_; ++c)
      buffer_.copyFrom(c, b.first, samples[c] + total, size);
    total += size;
  }
  return total == count;
}

bool RingBuffer::write(const AudioSampleBuffer& buffer) {
  auto samples = const_cast<const float**>(buffer.getArrayOfChannels());
  return write(buffer.getNumSamples(), samples);
}

bool RingBuffer::read(const AudioSourceChannelInfo& info) {
  auto count = info.numSamples;
  auto blocks = index_->read(count);
  auto total = 0;
  auto buf = info.buffer;
  for (auto& b: blocks) {
    auto size = b.second - b.first;
    for (auto c = 0; c < channels_; ++c)
      buf->copyFrom(c, info.startSample + total, buffer_, c, b.first, size);
    total += size;
  }
  return total == count;
}

bool RingBuffer::read(AudioSampleBuffer* buffer) {
  return read(AudioSourceChannelInfo(buffer, 0, buffer->getNumSamples()));
}

int RingBuffer::available() const {
  ScopedLock l(lock_);
  return index_->available();
}

int RingBuffer::size() const {
  return index_->size();
}

}  // namespace audio
}  // namespace echomesh

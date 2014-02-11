#include <limits>

#include "echomesh/audio/Loudness.h"

namespace echomesh {
namespace audio {

Loudness::Loudness(uint windowSize)
    : windowSize_(windowSize),
      sum_(0),
      loudness_(-std::numeric_limits<float>::infinity()) {}

void Loudness::callback(int channels, int count, const float** samples) {
  for (int i = 0; i < count; ++i) {
    for (int j = 0; j < channels; ++j) {
      auto s = samples[j][i];
      sum_ += s * s;
    }
    if (++sampleIndex_ >= windowSize_) {
      auto loudness = logf(sqrtf(sum_));
      sampleIndex_ = 0;
      sum_ = 0;
      ScopedLock l(lock_);
      loudness_ = loudness;
    }
  }
}

float Loudness::loudness() const {
  ScopedLock l(lock_);
  return loudness_;
}

}  // namespace audio
}  // namespace echomesh

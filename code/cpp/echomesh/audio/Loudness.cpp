#include <limits>

#include "echomesh/audio/Input.h"
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

class LoudnessInput : public Loudness {
 public:
  explicit LoudnessInput(const string& name, int channels, uint windowSize)
      : Loudness(windowSize),
        input_(getInput(name, channels)) {
    if (hasInput())
      input_->addCallback(this);
  }

  ~LoudnessInput() {
    if (hasInput())
      input_->removeCallback(this);
  }

  bool hasInput() const { return input_.get(); }

 private:
  std::shared_ptr<Input> input_;
};

unique_ptr<Loudness> loudnessInput(
    const string& name, int channels, uint windowSize) {
  unique_ptr<LoudnessInput> result(
      new LoudnessInput(name, channels, windowSize));
  if (not result->hasInput())
    result.reset();

  return unique_ptr<Loudness>(result.release());
}

}  // namespace audio
}  // namespace echomesh

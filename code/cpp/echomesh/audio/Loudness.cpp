#include <limits>

#include "echomesh/audio/Input.h"
#include "echomesh/audio/Loudness.h"

namespace echomesh {
namespace audio {

Loudness::Loudness(int chunkSize)
        : chunkSize_(chunkSize),
          sum_(0),
          loudness_(-std::numeric_limits<float>::infinity()) {}

void Loudness::callback(int channels, int count, const float** samples) {
    for (int i = 0; i < count; ++i) {
        for (int j = 0; j < channels; ++j) {
            auto s = samples[j][i];
            sum_ += s * s;
        }
        if (++sampleIndex_ >= chunkSize_) {
            auto loudness = 10.f * logf(sqrtf(sum_ / (channels * chunkSize_)));
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
    LoudnessInput(
        const string& name, int channels, int chunkSize, int sampleRate)
            : Loudness(chunkSize),
              input_(getInput(name, channels, sampleRate)) {
        if (hasInput())
            input_->addCallback(this);
    }

    ~LoudnessInput() override {
        if (hasInput())
            input_->removeCallback(this);
    }

    bool hasInput() const { return input_.get(); }

  private:
    std::shared_ptr<Input> input_;
};

Loudness* loudnessInput(const string& name, int channels, int chunkSize,
                        int sampleRate) {
    unique_ptr<LoudnessInput> result(
        new LoudnessInput(name, channels, chunkSize, sampleRate));
    return result->hasInput() ? result.release() : nullptr;
}

}  // namespace audio
}  // namespace echomesh

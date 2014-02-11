#pragma once

#include "echomesh/audio/InputCallback.h"

namespace echomesh {
namespace audio {

class Loudness : public InputCallback {
 public:
  explicit Loudness(uint windowSize);
  void callback(int channels, int count, const float** samples) override;
  float loudness() const;

 private:
  uint sampleIndex_;
  const uint windowSize_;
  float sum_;
  float loudness_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Loudness);
};

unique_ptr<Loudness> loudnessInput(
    const string& name, int channels, uint windowSize);

}  // namespace audio
}  // namespace echomesh

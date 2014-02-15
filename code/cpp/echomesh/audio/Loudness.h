#pragma once

#include "echomesh/audio/InputCallback.h"

namespace echomesh {
namespace audio {

class Loudness : public InputCallback {
 public:
  explicit Loudness(int chunkSize);
  void callback(int channels, int count, const float** samples) override;
  float loudness() const;

 private:
  int sampleIndex_;
  const int chunkSize_;
  float sum_;
  float loudness_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Loudness);
};

Loudness* loudnessInput(
    const string& name, int channels, int chunkSize, int sampleRate);

}  // namespace audio
}  // namespace echomesh

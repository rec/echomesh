#include "rec/audio/OutputSampleRate.h"

namespace rec {
namespace audio {

namespace {

struct SampleRateSingleton {
  SampleRateSingleton() : sampleRate_(44100) {}

  CriticalSection lock_;
  SampleRate sampleRate_;
  Broadcaster<SampleRate> broadcaster_;
};

inline SampleRateSingleton* outputRate() {
  static SampleRateSingleton out;
  return &out;
}

}  // namespace

SampleRate getOutputSampleRate() {
  Lock l(outputRate()->lock_);
  return outputRate()->sampleRate_;
}

void setOutputSampleRate(SampleRate st) {
  {
    Lock l(outputRate()->lock_);
    outputRate()->sampleRate_ = st;
  }
  getOutputSampleRateBroadcaster()->broadcast(st);
}

Broadcaster<SampleRate>* getOutputSampleRateBroadcaster() {
  return &outputRate()->broadcaster_;
}

}  // namespace audio
}  // namespace rec


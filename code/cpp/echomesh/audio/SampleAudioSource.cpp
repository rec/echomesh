#include "echomesh/audio/SampleAudioSource.h"

namespace echomesh {

SampleAudioSource::SampleAudioSource(const Node& node) {
  node >> playback_;
}

SampleAudioSource::~SampleAudioSource() {}

void SampleAudioSource::prepareToPlay(int samplesPerBlockExpected,
                                      double sampleRate) {
}

void SampleAudioSource::releaseResources() {}

void SampleAudioSource::getNextAudioBlock(const AudioSourceChannelInfo& buf) {
  buf.clearActiveBufferRegion();
}

void SampleAudioSource::run() {}
void SampleAudioSource::begin() {}
void SampleAudioSource::pause() {}
void SampleAudioSource::unload() {}

}  // namespace echomesh


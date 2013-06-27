#include "echomesh/audio/EnvelopeAudioSource.h"

namespace echomesh {

EnvelopeAudioSource::EnvelopeAudioSource(const YAML::Node&) {

}

EnvelopeAudioSource::~EnvelopeAudioSource() {}

void EnvelopeAudioSource::prepareToPlay(int samplesPerBlockExpected,
                                        double sampleRate) {
}

void EnvelopeAudioSource::releaseResources() {}

void EnvelopeAudioSource::getNextAudioBlock(const AudioSourceChannelInfo& buf) {
  buf.clearActiveBufferRegion();
}

void EnvelopeAudioSource::run() {}
void EnvelopeAudioSource::begin() {}
void EnvelopeAudioSource::pause() {}
void EnvelopeAudioSource::unload() {}

}  // namespace echomesh


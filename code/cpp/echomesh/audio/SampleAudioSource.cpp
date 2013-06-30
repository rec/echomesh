#include "echomesh/audio/SampleAudioSource.h"
#include "echomesh/audio/GetReader.h"

namespace echomesh {

SampleAudioSource::SampleAudioSource(const Node& node) : isRunning_(false) {
  node >> playback_;
  source_ = getReader(playback_.file, playback_.begin, playback_.end);
}

SampleAudioSource::~SampleAudioSource() {}

void SampleAudioSource::prepareToPlay(int samplesPerBlockExpected,
                                      double sampleRate) {
  if (source_)
    source_->prepareToPlay(samplesPerBlockExpected, sampleRate);
}

void SampleAudioSource::releaseResources() {
  if (source_)
    source_->releaseResources();
}

void SampleAudioSource::getNextAudioBlock(const AudioSourceChannelInfo& buf) {
  if (source_) {
  } else {
    buf.clearActiveBufferRegion();
  }
}

void SampleAudioSource::run() {
}

void SampleAudioSource::begin() {
}

void SampleAudioSource::pause() {
}

void SampleAudioSource::unload() {
}

}  // namespace echomesh


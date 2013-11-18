#include "echomesh/audio/SampleAudioSource.h"
#include "echomesh/audio/GetReader.h"

namespace echomesh {

SampleAudioSource::SampleAudioSource(const Node& node) : length_(0) {
  Playback playback;
  node >> playback;

  init(playback.filename, playback.loops, playback.begin, playback.end, playback.length);
}

void SampleAudioSource::init(
    const String& filename, int loops,
    SampleTime begin, SampleTime end, SampleTime length) {
  source_.reset(getReader(filename, begin, end));
  if (source_)
    length_ = jmin(SampleTime(source_->getTotalLength() * loops), length);
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
  ScopedLock l(lock_);
  if (not (source_ and isRunning_)) {
    buf.clearActiveBufferRegion();
    return;
  }

  currentTime_ += buf.numSamples;
  SampleTime overrun(currentTime_ - length_);
  if (overrun < 0) {
    source_->getNextAudioBlock(buf);
    return;
  }

  AudioSourceChannelInfo b = buf;
  b.numSamples -= overrun;
  source_->getNextAudioBlock(b);
  b.startSample += b.numSamples;
  b.numSamples = overrun;
  b.clearActiveBufferRegion();
  isRunning_ = false;
}

void SampleAudioSource::run() {
  ScopedLock l(lock_);
  isRunning_ = true;
}

void SampleAudioSource::begin() {
  ScopedLock l(lock_);
  currentTime_ = 0;
  if (source_)
    source_->setNextReadPosition(0);
}

void SampleAudioSource::pause() {
  ScopedLock l(lock_);
  isRunning_ = false;
}

void SampleAudioSource::unload() {
  ScopedLock l(lock_);
  releaseResources();
  source_ = NULL;
  isRunning_ = false;
}

}  // namespace echomesh


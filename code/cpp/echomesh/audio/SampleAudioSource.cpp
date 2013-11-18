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
  if (source_) {
    length_ = SampleTime(source_->getTotalLength() * loops);
    if (length_ >= 0)
      length_ = jmin(length_, length);
  }
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
    float max, min;
    buf.buffer->findMinMax(0, buf.startSample, buf.numSamples, min, max);
    DLOG(INFO) << "!! " << min << ", " << max;
    return;
  }

  AudioSourceChannelInfo b = buf;
  b.numSamples -= overrun;
  DLOG(INFO) << "prepare to get next audio block!!";
  source_->getNextAudioBlock(b);
  DLOG(INFO) << "got next audio block!!";
  b.startSample += b.numSamples;
  b.numSamples = overrun;
  b.clearActiveBufferRegion();
  isRunning_ = false;
}

void SampleAudioSource::run() {
  ScopedLock l(lock_);
  std::cerr << "running!!\n";
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


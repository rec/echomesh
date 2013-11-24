#include <math.h>

#include "echomesh/audio/SampleAudioSource.h"
#include "echomesh/audio/GetReader.h"
#include "echomesh/util/InitLog.h"

namespace echomesh {
namespace audio {

SampleAudioSource::SampleAudioSource(const Node& node) :
    length_(0), gain_(), pan_(), callback_(nullptr), callbackData_(nullptr) {
  Playback playback;
  node >> playback;

  init(playback.filename, playback.loops,
       playback.begin, playback.end, playback.length, nullptr, nullptr);
}

SampleAudioSource::SampleAudioSource(
    const String& filename, int loops,
    SampleTime begin, SampleTime end, SampleTime length,
    Envelope* gain, Envelope* pan,
    AppCallback callback, void* callbackData)
    : gain_(gain),
      pan_(pan),
      callback_(callback),
      callbackData_(callbackData) {
  init(filename, loops, begin, end, length, gain, pan);
}


void SampleAudioSource::init(
    const String& filename, int loops,
    SampleTime begin, SampleTime end, SampleTime length,
    Envelope* gain, Envelope* pan) {
  source_ = getReader(filename, begin, end);
  if (source_) {
    length_ = SampleTime(source_->getTotalLength() * loops);
    if (length >= 0)
      length_ = jmin(length_, length);
  } else {
    const char* error = File(filename).exists() ?
        "Don't understand file format for " :
        "File doesn't exist: ";
    error_ = (error + filename).toStdString();
  }
  panGainPlayer_ = make_unique<PanGainPlayer>(gain, pan);
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
    panGainPlayer_->apply(buf);
    return;
  }

  AudioSourceChannelInfo b = buf;
  b.numSamples -= overrun;
  source_->getNextAudioBlock(b);
  panGainPlayer_->apply(b);
  b.startSample += b.numSamples;
  b.numSamples = overrun;
  b.clearActiveBufferRegion();
  isRunning_ = false;
  callback_(callbackData_);
  // Might block - perhaps we should do this in another thread?
}

void SampleAudioSource::run() {
  ScopedLock l(lock_);
  isRunning_ = true;
}

void SampleAudioSource::begin() {
  ScopedLock l(lock_);
  panGainPlayer_->begin();

  currentTime_ = 0;
  if (source_)
    source_->setNextReadPosition(0);
}

void SampleAudioSource::pause() {
  ScopedLock l(lock_);
  isRunning_ = false;
}

}  // namespace audio
}  // namespace echomesh


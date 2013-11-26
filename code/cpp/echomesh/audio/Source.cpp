#include "echomesh/audio/Source.h"
#include "echomesh/audio/AudioPlayer.h"

namespace echomesh {
namespace audio {

Source::Source(const string& filename, int loops,
               double begin, double end, double length,
               const string& device, int channels,
               Envelope* gain, Envelope* pan,
               VoidCaller callback, void* callbackData,
               float sampleRate)
    : SampleAudioSource(filename, loops,
                        SampleTime(begin, sampleRate),
                        SampleTime(end, sampleRate),
                        SampleTime(length, sampleRate), gain, pan,
                        callback, callbackData, sampleRate, channels),
      player_(AudioPlayer::getPlayer(device, channels))  {
  callback(callbackData);
  player_->addInputSource(this);
}

Source::~Source() {
  pause();
  if (player_->removeInputSource(this))
    AudioPlayer::removePlayer(player_);
}

}  // namespace audio
}  // namespace echomesh

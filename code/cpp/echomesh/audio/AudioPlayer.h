#ifndef __ECHOMESH_AUDIOPLAYER__
#define __ECHOMESH_AUDIOPLAYER__

#include <unordered_set>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class AudioPlayer {
 public:
  static AudioPlayer* getPlayer(const string& name, int channels);

  ~AudioPlayer() {}

  const String& error() const { return error_; }
  MixerAudioSource* source() { return &mixer_; }

 private:
  AudioPlayer(const string& name, int channels);

  const string name_;
  const int channels_;
  String error_;

  AudioSourcePlayer player_;
  AudioDeviceManager manager_;
  MixerAudioSource mixer_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(AudioPlayer);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_AUDIOPLAYER__

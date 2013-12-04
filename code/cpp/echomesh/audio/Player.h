#ifndef __ECHOMESH_PLAYER__
#define __ECHOMESH_PLAYER__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class Player {
 public:
  Player() {}

  void initialize(AudioSource* source = NULL) {
    String err = manager_.initialise(1, 2, NULL, true);
    if (err.length()) {
      DLOG(INFO) << "Couldn't initialize audio::Device, error "
                 <<  err.toStdString();
    }
    player_.setSource(source);
    manager_.addAudioCallback(&player_);
  }

 private:
  AudioSourcePlayer player_;
  AudioDeviceManager manager_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Player);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_PLAYER__

#ifndef __ECHOMESH_PLAYER__
#define __ECHOMESH_PLAYER__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class Player {
 public:
  Player() {}

  void initialize() {
    String err = manager_.initialise(1, 2, NULL, true);
    if (err.length())
      log(String("Couldn't initialize audio::Device, error ") + err);
    player_.setSource(&source_);
    manager_.addAudioCallback(&player_);
  }

  MixerAudioSource* source() { return &source_; }

 private:
  MixerAudioSource source_;
  AudioSourcePlayer player_;
  AudioDeviceManager manager_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Player);
};

}  // namespace echomesh

#endif  // __ECHOMESH_PLAYER__

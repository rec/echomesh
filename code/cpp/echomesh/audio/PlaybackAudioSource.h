#ifndef __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__
#define __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class PlaybackAudioSource : public AudioSource {
 public:
  PlaybackAudioSource() : count_(0) {}

  virtual void prepareToPlay(int /*samplesPerBlockExpected*/,
                             double /*sampleRate*/) {
  }
  virtual void releaseResources() {}


  virtual void getNextAudioBlock(const AudioSourceChannelInfo& block) {
    block.clearActiveBufferRegion();
    if (not count_++)
      log("playing back!");
  }

 private:
  int count_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PlaybackAudioSource)
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

#ifndef __ECHOMESH_AUDIO_CONTROLLER__
#define __ECHOMESH_AUDIO_CONTROLLER__

#include <map>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class PlaybackAudioSource;
class SampleAudioSource;

class AudioController {
 public:
  AudioController(Node*, PlaybackAudioSource*);
  virtual ~AudioController();

  void audio();

 private:
  typedef uint64 Hash;
  typedef std::map<Hash, SampleAudioSource*> Sources;

  Sources sources_;
  Node* node_;
  PlaybackAudioSource* playbackAudioSource_;

  DISALLOW_COPY_AND_ASSIGN(AudioController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_CONTROLLER__

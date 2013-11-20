#ifndef __ECHOMESH_AUDIO_CONTROLLER__
#define __ECHOMESH_AUDIO_CONTROLLER__

#include <map>

#include "echomesh/base/Config.h"

namespace echomesh {
namespace audio {

class SampleAudioSource;

class AudioController {
 public:
  explicit AudioController(const Node&);
  virtual ~AudioController() {}

  void audio();
  AudioSource* source() { return &mixerAudioSource_; }

 private:
  typedef uint64 Hash;
  typedef std::map<Hash, audio::SampleAudioSource*> Sources;

  Sources sources_;
  const Node& node_;
  MixerAudioSource mixerAudioSource_;

  DISALLOW_COPY_AND_ASSIGN(AudioController);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_CONTROLLER__

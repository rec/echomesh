#ifndef __ECHOMESH_AUDIO_CONTROLLER__
#define __ECHOMESH_AUDIO_CONTROLLER__

#include <map>

#include "echomesh/base/Echomesh.h"

namespace YAML { class Node; }

namespace echomesh {

class EnvelopeAudioSource;

class AudioController {
 public:
  AudioController(YAML::Node*);
  virtual ~AudioController();

  void audio();

 private:
  typedef uint64 Hash;
  typedef std::map<Hash, EnvelopeAudioSource*> Sources;
  Sources sources_;

  YAML::Node* node_;
  DISALLOW_COPY_AND_ASSIGN(AudioController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_CONTROLLER__

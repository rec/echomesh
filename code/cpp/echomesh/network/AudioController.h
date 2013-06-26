#ifndef __ECHOMESH_AUDIO_CONTROLLER__
#define __ECHOMESH_AUDIO_CONTROLLER__

#include <stdio.h>

#include "echomesh/base/Echomesh.h"

namespace YAML { class Node; }

namespace echomesh {

class AudioController {
 public:
  AudioController(YAML::Node*);
  virtual ~AudioController();

  void audio();

 private:
  YAML::Node* node_;
  DISALLOW_COPY_AND_ASSIGN(AudioController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_CONTROLLER__

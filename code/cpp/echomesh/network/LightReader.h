#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/base/Config.h"
#include "echomesh/network/ReadThread.h"

namespace echomesh {

namespace audio {
class AudioController;
class MidiController;
}

class LightingWindow;
class LightController;

class LightReader : public ReadThread {
 public:
  LightReader();
  virtual ~LightReader();
  void initialize(LightingWindow*);

  AudioSource* source();

 private:
  void config();

  ScopedPointer<audio::AudioController> audioController_;
  ScopedPointer<LightController> lightController_;
  ScopedPointer<audio::MidiController> midiController_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__

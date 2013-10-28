#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/base/Config.h"
#include "echomesh/network/ReadThread.h"

namespace echomesh {

class AudioController;
class LightingWindow;
class LightController;
class MidiController;

class LightReader : public ReadThread {
 public:
  LightReader();
  virtual ~LightReader();
  void initialize(LightingWindow*);

  AudioSource* source();

 private:
  void config();

  ScopedPointer<AudioController> audioController_;
  ScopedPointer<LightController> lightController_;
  ScopedPointer<MidiController> midiController_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__

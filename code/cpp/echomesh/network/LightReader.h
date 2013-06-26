#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/base/Config.h"
#include "echomesh/network/ReadThread.h"

namespace echomesh {

class LightingWindow;
class ConfigMidiInput;
class ConfigMidiOutput;
class LightController;
class MidiController;

class LightReader : public ReadThread, public MidiInputCallback {
 public:
  LightReader(LightingWindow* window, const String& commandLine);
  virtual ~LightReader();

 private:
  virtual void quit();
  void audio();
  void clear();
  void config();
  void displayLights();
  void enforceSizes();
  void light();
  void midi();

  ScopedPointer<LightController> lightController_;
  ScopedPointer<MidiController> midiController_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};


}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__

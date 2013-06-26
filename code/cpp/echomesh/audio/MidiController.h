#ifndef __ECHOMESH_MIDI_CONTROLLER__
#define __ECHOMESH_MIDI_CONTROLLER__

#include <stdio.h>

#include "echomesh/base/Echomesh.h"

namespace YAML { class Node; }

namespace echomesh {

class ConfigMidiInput;
class ConfigMidiOutput;

class MidiController : public MidiInputCallback {
 public:
  MidiController(YAML::Node*);
  virtual ~MidiController();
  virtual void handleIncomingMidiMessage(MidiInput*, const MidiMessage&);

  void config();
  void midi();

 private:
  YAML::Node* node_;
  ScopedPointer<ConfigMidiInput> midiInput_;
  ScopedPointer<ConfigMidiOutput> midiOutput_;

  DISALLOW_COPY_AND_ASSIGN(MidiController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_MIDI_CONTROLLER__

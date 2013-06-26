#ifndef __ECHOMESH_MIDI_CONTROLLER__
#define __ECHOMESH_MIDI_CONTROLLER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/util/GetDevice.h"

namespace echomesh {

class MidiController : public MidiInputCallback {
 public:
  MidiController(YAML::Node* node) : node_(node), midiInput_(this) {}
  virtual ~MidiController() {}
  virtual void handleIncomingMidiMessage(MidiInput*, const MidiMessage&);

  void config();
  void midi();

 private:
  YAML::Node* node_;
  ConfigMidiInput midiInput_;
  ConfigMidiOutput midiOutput_;

  DISALLOW_COPY_AND_ASSIGN(MidiController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_MIDI_CONTROLLER__

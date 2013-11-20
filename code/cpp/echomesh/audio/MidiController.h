#ifndef __ECHOMESH_MIDI_CONTROLLER__
#define __ECHOMESH_MIDI_CONTROLLER__

#include <stdio.h>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class ConfigMidiInput;
class ConfigMidiOutput;

class MidiController : public MidiInputCallback {
 public:
  MidiController(const Node&);
  virtual ~MidiController();
  virtual void handleIncomingMidiMessage(MidiInput*, const MidiMessage&);

  void config();
  void midi();

 private:
  const Node& node_;
  ScopedPointer<ConfigMidiInput> midiInput_;
  ScopedPointer<ConfigMidiOutput> midiOutput_;

  DISALLOW_COPY_AND_ASSIGN(MidiController);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_MIDI_CONTROLLER__

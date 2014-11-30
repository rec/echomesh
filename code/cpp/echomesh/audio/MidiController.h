#pragma once

#include <stdio.h>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class ConfigMidiInput;
class ConfigMidiOutput;

class MidiController : public MidiInputCallback {
  public:
    MidiController();
    virtual ~MidiController();
    virtual void handleIncomingMidiMessage(MidiInput*, const MidiMessage&);

    void config();
    void midi();

  private:
#if 0
    ScopedPointer<ConfigMidiInput> midiInput_;
    ScopedPointer<ConfigMidiOutput> midiOutput_;
#endif

    DISALLOW_COPY_AND_ASSIGN(MidiController);
};

}  // namespace audio
}  // namespace echomesh


#ifndef __ECHOMESH_GET_DEVICE__
#define __ECHOMESH_GET_DEVICE__

#include <queue>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class OneMidiConfig;

MidiInput* openMidiInput(const OneMidiConfig&, MidiInputCallback*);
MidiOutput* openMidiOutput(const OneMidiConfig&);

}  // namespace echomesh

#endif  // __ECHOMESH_GET_DEVICE__

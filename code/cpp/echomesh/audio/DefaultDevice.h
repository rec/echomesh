#ifndef __ECHOMESH_DEFAULTDEVICE__
#define __ECHOMESH_DEFAULTDEVICE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

double defaultInputSampleRate();
double defaultOutputSampleRate();
string defaultInputDevice();
string defaultOutputDevice();

vector<string> getDeviceNames(bool wantInputs);

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_DEFAULTDEVICE__

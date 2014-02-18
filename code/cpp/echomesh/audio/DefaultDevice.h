#pragma once

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

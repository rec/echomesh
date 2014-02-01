#ifndef __ECHOMESH_DEFAULTDEVICE__
#define __ECHOMESH_DEFAULTDEVICE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

double defaultInputSampleRate();
double defaultOutputSampleRate();
string defaultInputDevice();
string defaultOutputDevice();

struct DeviceDeleter {
  void operator()(AudioDeviceManager*);
};

typedef unique_ptr<AudioDeviceManager, DeviceDeleter> AudioDeviceManagerPointer;

AudioDeviceManagerPointer getDevice(
    bool isInput, const string& name = "", int channels = 2);

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_DEFAULTDEVICE__

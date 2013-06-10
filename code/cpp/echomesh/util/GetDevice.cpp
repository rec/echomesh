#include "echomesh/util/GetDevice.h"
#include "echomesh/base/Config.h"

namespace echomesh {

namespace {

template <typename DeviceClass>
int getDeviceIndex(const String& name, int index) {
  StringArray names = DeviceClass::getDevices();
  if (index >= 0)
    return index < names.size() ? index : -1;

  index = names.indexOf(name);
  if (index < 0) {
    for (int i = 0; i < names.size(); ++i) {
      if (names[i].startsWith(name))
        return i;
    }
    index = DeviceClass::getDefaultDeviceIndex();
  }

  return index;
}


template <typename DeviceClass>
int getDeviceIndex(const OneMidiConfig& config) {
  if (not config.external)
    return -1;
  return getDeviceIndex<DeviceClass>(String(config.name), config.index);
}

}  // namespace

MidiInput* openMidiInput(const OneMidiConfig& config,
                         MidiInputCallback* callback) {
  int index = getDeviceIndex<MidiInput>(config);
  return index >= 0 ? MidiInput::openDevice(index, callback) : NULL;
}

MidiOutput* openMidiOutput(const OneMidiConfig& config) {
  int index = getDeviceIndex<MidiOutput>(config);
  return index >= 0 ? MidiOutput::openDevice(index) : NULL;
}

}  // namespace echomesh


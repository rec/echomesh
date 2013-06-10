#include "echomesh/util/GetDevice.h"
#include "echomesh/base/Config.h"

namespace echomesh {

namespace {

template <typename DeviceClass>
int getDeviceIndex(const String& name, int index) {
  StringArray names = DeviceClass::getDevices();
  log(names.joinIntoString(", "));
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

MidiInput* openMidiInput(const OneMidiConfig& config,
                         MidiInputCallback* callback) {
  int index = getDeviceIndex<MidiInput>(config);
  return index >= 0 ? MidiInput::openDevice(index, callback) : NULL;
}

MidiOutput* openMidiOutput(const OneMidiConfig& config) {
  int index = getDeviceIndex<MidiOutput>(config);
  return index >= 0 ? MidiOutput::openDevice(index) : NULL;
}

class CallbackContainer : public MidiInputCallback {
 public:
  explicit CallbackContainer(MidiInputCallback* cb) : callback_(cb) {}

  virtual void handleIncomingMidiMessage(MidiInput* source,
                                         const MidiMessage& message) {
    if (callback_)
      callback_->handleIncomingMidiMessage(source, message);
  }

  virtual void handlePartialSysexMessage(MidiInput* src,
                                         const uint8* msg,
                                         int bytes,
                                         double ts) {
    if (callback_)
      callback_->handlePartialSysexMessage(src, msg, bytes, ts);
  }

 private:
  MidiInputCallback* callback_;
};

}  // namespace

bool equals(const OneMidiConfig& x, const OneMidiConfig& y) {
  return x.external == y.external and x.index == y.index and x.name == y.name;
}

MidiInput* ConfigMidiInput::newDevice() {
  int index = getDeviceIndex<MidiInput>(config_);
  return index >= 0 ?
    MidiInput::openDevice(index, new CallbackContainer(callback_.get())) :  NULL;
}

MidiOutput* ConfigMidiOutput::newDevice() {
  int index = getDeviceIndex<MidiOutput>(config_);
  return index >= 0 ? MidiOutput::openDevice(index) : NULL;
}

void ConfigMidiOutput::sendMessageNow(const MidiMessage& msg) {
  if (device_)
    device_->sendMessageNow(msg);
}

}  // namespace echomesh

#if 0
#include "echomesh/util/GetDevice.h"

namespace echomesh {
namespace audio {

namespace {

template <typename DeviceClass>
int getDeviceIndex(const String& name, int index) {
  auto names = DeviceClass::getDevices();
  if (index >= 0) {
    index = jmin(index, names.size() - 1);
  } else {
    index = names.indexOf(name);
    if (index < 0) {
      for (int i = 0; i < names.size(); ++i) {
        if (names[i].startsWith(name)) {
          index = i;
          break;
        }
      }
    }
    if (index < 0)
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
  auto index = getDeviceIndex<MidiInput>(config);
  return index >= 0 ? MidiInput::openDevice(index, callback) : NULL;
}

MidiOutput* openMidiOutput(const OneMidiConfig& config) {
  auto index = getDeviceIndex<MidiOutput>(config);
  return index >= 0 ? MidiOutput::openDevice(index) : NULL;
}

class CallbackContainer : public MidiInputCallback {
 public:
  explicit CallbackContainer(MidiInputCallback* cb) : callback_(cb) {}

  virtual void handleIncomingMidiMessage(MidiInput* source,
                                         const MidiMessage& message) {
    // log("FIRST handleIncomingMidiMessage");
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
  if (auto input = openMidiInput(config_, new CallbackContainer(callback_))) {
    input->start();
    return input;
  }
  return nullptr;
}

MidiOutput* ConfigMidiOutput::newDevice() {
  return openMidiOutput(config_);
}

void ConfigMidiOutput::sendMessageNow(const MidiMessage& msg) {
  if (device_)
    device_->sendMessageNow(msg);
}

}  // namespace audio
}  // namespace echomesh
#endif

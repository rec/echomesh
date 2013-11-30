#ifndef __ECHOMESH_GET_DEVICE__
#define __ECHOMESH_GET_DEVICE__

#include <queue>

#include "echomesh/base/Config.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {
namespace audio {

bool equals(const OneMidiConfig&, const OneMidiConfig&);

class CallbackWrapper : public CallbackMessage {
 public:
  explicit CallbackWrapper(CallbackMessage* cb) : callback_(cb) {}

  virtual void messageCallback() {
    callback_->messageCallback();
  }

 private:
  CallbackMessage* const callback_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackWrapper);
};

template <typename DeviceClass>
class ConfigMidi : public CallbackMessage {
 public:
  ConfigMidi() : configAssigned_(false) {}
  virtual ~ConfigMidi() {}

  void setConfig(const OneMidiConfig& config) {
    if (not (configAssigned_ and equals(config_, config))) {
      configAssigned_ = true;
      config_ = config;

      runOnMessageThread(&ConfigMidi<DeviceClass>::messageCallback, this);
    }
  }

  virtual void messageCallback() {
    device_ = config_.external ? newDevice() : NULL;
  }

  virtual DeviceClass* newDevice() = 0;

  OneMidiConfig config_;
  ScopedPointer<DeviceClass> device_;

 private:
  bool configAssigned_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(ConfigMidi);
};

class ConfigMidiInput : public ConfigMidi<MidiInput> {
 public:
  explicit ConfigMidiInput(MidiInputCallback* cb) : callback_(cb) {}

 protected:
  virtual MidiInput* newDevice();

 private:
  MidiInputCallback* callback_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(ConfigMidiInput);
};


class ConfigMidiOutput : public ConfigMidi<MidiOutput> {
 public:
  ConfigMidiOutput() {}
  void sendMessageNow(const MidiMessage&);

 protected:
  virtual MidiOutput* newDevice();

 private:
  DISALLOW_COPY_ASSIGN_AND_LEAKS(ConfigMidiOutput);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_GET_DEVICE__

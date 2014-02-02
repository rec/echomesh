#include <map>
#include <tuple>

#include "echomesh/audio/DefaultDevice.h"

using namespace std;

namespace echomesh {
namespace audio {

namespace {

typedef AudioDeviceManager::AudioDeviceSetup AudioDeviceSetup;

AudioDeviceSetup defaultDeviceSetup(bool isOutput) {
  AudioDeviceManager manager;
  auto result = manager.initialise(
      isOutput ? 0 : 2,
      isOutput ? 2 : 0,
      nullptr,
      true);
  AudioDeviceSetup setup;
  manager.getAudioDeviceSetup(setup);
  return setup;
}

const AudioDeviceSetup& defaultInputSetup() {
  static const auto SETUP = defaultDeviceSetup(false);
  return SETUP;
}

const AudioDeviceSetup& defaultOutputSetup() {
  static const auto SETUP = defaultDeviceSetup(true);
  return SETUP;
}

typedef tuple<bool, string, int> DeviceID;

struct Device {
  unique_ptr<AudioDeviceManager> manager_;
  int referenceCount_;
};

typedef map<DeviceID, Device> DeviceTable;

CriticalSection DEVICE_LOCK;
static DeviceTable DEVICE_TABLE;

}  // namespace

void DeviceDeleter::operator()(AudioDeviceManager* dm) {
  ScopedLock l(DEVICE_LOCK);
  for (auto& i: DEVICE_TABLE) {
    auto& device = i.second;
    if (device.manager_.get() == dm) {
      if (not --device.referenceCount_)
        DEVICE_TABLE.erase(i.first);
      return;
    }
  }
}

AudioDeviceManagerPointer getDevice(
    bool isInput, const string& name, int channels) {
  ScopedLock l(DEVICE_LOCK);

  AudioDeviceManagerPointer result;
  DeviceID id(isInput, name, channels);
  auto i = DEVICE_TABLE.find(id);
  if (i != DEVICE_TABLE.end()) {
    auto& device = i->second;
    device.referenceCount_++;
    result.reset(device.manager_.get());
  } else {
    Device device;
    device.referenceCount_ = 1;
    device.manager_ = make_unique<AudioDeviceManager>();
    String error = device.manager_->initialise(
        isInput ? channels : 0, isInput ? 0 : channels,
        nullptr, false, name);

    if (error.length()) {
      LOG(DFATAL) << "Couldn't initialize " << name << " for "
                  << (isInput ? "input." : "output.");
    } else {
      result.reset(device.manager_.get());
      DEVICE_TABLE[id] = move(device);
    }
  }
  return result;
}


string defaultOutputDevice() {
  return defaultOutputSetup().outputDeviceName.toStdString();
}

string defaultInputDevice() {
  return defaultInputSetup().inputDeviceName.toStdString();
}

double defaultInputSampleRate() {
  return defaultInputSetup().sampleRate;
}

double defaultOutputSampleRate() {
  return defaultInputSetup().sampleRate;
}

}  // namespace audio
}  // namespace echomesh

#include <unordered_map>

#include "echomesh/audio/DefaultDevice.h"

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

struct Device {
  unique_ptr<AudioDeviceManager> manager_;
  int referenceCount_;
};

typedef std::unordered_map<string, Device> DeviceTable;

static DeviceTable DEVICE_TABLE;

}  // namespace

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

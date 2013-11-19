#include <unordered_map>

#include "echomesh/audio/DefaultDevice.h"

namespace echomesh {
namespace audio {

namespace {

typedef AudioDeviceManager::AudioDeviceSetup AudioDeviceSetup;

AudioDeviceSetup defaultDeviceSetup(bool isOutput) {
  AudioDeviceManager manager;
  String result = manager.initialise(
      isOutput ? 0 : 2,
      isOutput ? 2 : 0,
      nullptr,
      true);
  AudioDeviceSetup setup;
  manager.getAudioDeviceSetup(setup);
  return setup;
}

const AudioDeviceSetup& defaultInputSetup() {
  static const AudioDeviceSetup SETUP = defaultDeviceSetup(false);
  return SETUP;
}

const AudioDeviceSetup& defaultOutputSetup() {
  static const AudioDeviceSetup SETUP = defaultDeviceSetup(true);
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

AudioDeviceManager* cachedOutputManager(const string& name, int channels) {
  string n = name.empty() ? defaultOutputDevice() : name;
  auto i = DEVICE_TABLE.find(n);
  if (i == DEVICE_TABLE.end()) {
    Device device;
    device.referenceCount_ = 1;
    device.manager_ = make_unique<AudioDeviceManager>();
    String result = device.manager_->initialise(0, channels, nullptr, false, n);
    if (result.length()) {
      std::cerr << "Error opening device " << name << ": "
                << result.toStdString();
      return nullptr;
    }
    DEVICE_TABLE[name] = std::move(device);
    return device.manager_.get();
  }

  i->second.referenceCount_++;
  return i->second.manager_.get();
}

void dereferenceOutputManager(AudioDeviceManager* manager) {
  AudioDeviceManager::AudioDeviceSetup setup;
  manager->getAudioDeviceSetup(setup);
  string name = setup.outputDeviceName.toStdString();
  auto i = DEVICE_TABLE.find(name);
  if (i == DEVICE_TABLE.end())
    std::cerr << "Couldn't find device " << name;
  else if (not --i->second.referenceCount_)
    DEVICE_TABLE.erase(i);
}

string test1() {
  return "hello, Tylor!";
}

const char* test2() {
  return "hello, Tylor!";
}

}  // namespace audio
}  // namespace echomesh

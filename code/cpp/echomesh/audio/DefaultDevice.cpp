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

unique_ptr<AudioDeviceManager> outputManager(const string& name,
                                            int channels,
                                            double sampleRate) {
  unique_ptr<AudioDeviceManager> manager(new AudioDeviceManager);
  String result = manager->initialise(0, channels, nullptr, false, name);
  if (result.length()) {
    std::cerr << "Error opening device " << name << ": "
              << result.toStdString();
    manager = nullptr;
  }

  return std::move(manager);
}

}  // namespace audio
}  // namespace echomesh

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

}  // namespace audio
}  // namespace echomesh

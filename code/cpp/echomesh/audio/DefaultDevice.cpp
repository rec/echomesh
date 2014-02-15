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

vector<string> getDeviceNames(bool wantInputs = false) {
  vector<string> result;
  AudioDeviceManager manager;
  auto& types = manager.getAvailableDeviceTypes();
  for (auto& t: types) {
    t->scanForDevices();
    auto names = t->getDeviceNames(wantInputs);
    for (auto& name: names)
      result.push_back(name.trimEnd().toStdString());
  }
  return result;
}

}  // namespace audio
}  // namespace echomesh

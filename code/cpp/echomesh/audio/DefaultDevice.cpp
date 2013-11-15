#include "echomesh/audio/DefaultDevice.h"

namespace echomesh {
namespace audio {

namespace {

string defaultDevice(bool isOutput) {
  AudioDeviceManager manager;
  String result = manager.initialise(
      isOutput ? 0 : 2,
      isOutput ? 2 : 0,
      nullptr,
      true);
  if (result.isEmpty()) {
    AudioDeviceManager::AudioDeviceSetup setup;
    manager.getAudioDeviceSetup(setup);
    result = isOutput ? setup.outputDeviceName : setup.inputDeviceName;
  } else {
    result = "ERROR: " + result;
  }

  return result.toStdString();
}

}  // namespace

string defaultOutputDevice() {
  static const string DEVICE = defaultDevice(true);
  return DEVICE;
}


string defaultInputDevice() {
  static const string DEVICE = defaultDevice(false);
  return DEVICE;
}

}  // namespace audio
}  // namespace echomesh

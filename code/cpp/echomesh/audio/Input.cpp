#include "echomesh/audio/Input.h"

namespace echomesh {
namespace audio {

String Input::initialize(const string& name, int channels) {
  String error = manager_.initialise(channels, 0, nullptr, false, name);
  manager_.addAudioCallback(this);
  return error;
}

Input::~Input() {
  manager_.removeAudioCallback(this);
}

void Input::audioDeviceIOCallback (const float** inputChannelData,
                                   int numInputChannels,
                                   float** outputChannelData,
                                   int numOutputChannels,
                                   int numSamples) {
}

void Input::audioDeviceAboutToStart(AudioIODevice* device) {
}

void Input::audioDeviceStopped() {
}

void Input::audioDeviceError(const String& errorMessage) {
}

}  // namespace audio
}  // namespace echomesh

#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class Input : public AudioIODeviceCallback {
 public:
  Input() {}
  ~Input();

  String initialize(const string& name, int channels);

  void audioDeviceIOCallback (const float** inputChannelData,
                              int numInputChannels,
                              float** outputChannelData,
                              int numOutputChannels,
                              int numSamples) override;

  void audioDeviceAboutToStart(AudioIODevice* device) override;
  void audioDeviceStopped() override;
  void audioDeviceError(const String& errorMessage) override;

 private:
  AudioDeviceManager manager_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Input);
};

}  // namespace audio
}  // namespace echomesh

#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class Input : public AudioIODeviceCallback {
 public:
  class Callback {
   public:
    virtual ~Callback() {}
    virtual void callback(int channels, int count, const float** samples) = 0;
  };

  Input() {}
  ~Input();

  String initialize(const string& name, int channels);

  void audioDeviceIOCallback(const float** inputChannelData,
                             int numInputChannels,
                             float**, int,
                             int numSamples) override;

  void audioDeviceAboutToStart(AudioIODevice* device) override;
  void audioDeviceStopped() override;
  void audioDeviceError(const String& errorMessage) override;

  void addCallback(unique_ptr<Callback>);
  void removeCallback(Callback*);

 private:
  string name_;
  AudioDeviceManager manager_;
  std::vector<unique_ptr<Callback>> callbacks_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Input);
};

}  // namespace audio
}  // namespace echomesh

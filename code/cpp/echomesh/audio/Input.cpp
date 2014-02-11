#include "echomesh/audio/Input.h"
#include "echomesh/util/STL.h"

using namespace std;

namespace echomesh {
namespace audio {

String Input::initialize(const string& name, int channels) {
  name_ = name;
  String error = manager_.initialise(channels, 0, nullptr, false, name);
  manager_.addAudioCallback(this);
  return error;
}

Input::~Input() {
  manager_.removeAudioCallback(this);
}

void Input::audioDeviceIOCallback(const float** inputChannelData,
                                  int channels,
                                  float**,
                                  int,
                                  int numSamples) {
  ScopedLock l(lock_);
  for (auto& i: callbacks_)
    i->callback(channels, numSamples, inputChannelData);
}

void Input::audioDeviceAboutToStart(AudioIODevice* device) {
}

void Input::audioDeviceStopped() {
}

void Input::audioDeviceError(const String& errorMessage) {
  LOG(ERROR) << "Error on device " << name_
             << ": " << errorMessage.toStdString();
}

void Input::addCallback(unique_ptr<InputCallback> cb) {
  ScopedLock l(lock_);
  callbacks_.push_back(std::move(cb));
}

void Input::removeCallback(InputCallback* cb) {
  ScopedLock l(lock_);
  erasePointer(&callbacks_, cb);
}

}  // namespace audio
}  // namespace echomesh

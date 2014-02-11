#include <map>

#include "echomesh/audio/Input.h"

using namespace std;

namespace echomesh {
namespace audio {

namespace {

typedef map<InputID, Input*> InputTable;

CriticalSection INPUT_LOCK;
InputTable INPUT_TABLE;

class InputImpl : public AudioIODeviceCallback, public Input {
 public:
  InputImpl(const InputID& id) : id_(id) {}

  ~InputImpl() {
    manager_.removeAudioCallback(this);
  }

  String initialize() {
    String error = manager_.initialise(id_.second, 0, nullptr, false, id_.first);
    manager_.addAudioCallback(this);
    return error;
  }

  void audioDeviceIOCallback(const float** inputChannelData,
                             int channels,
                             float**, int,
                             int numSamples) override {
    ScopedLock l(lock_);
    for (auto& i: callbacks_)
      i->callback(channels, numSamples, inputChannelData);
  }

  void audioDeviceAboutToStart(AudioIODevice* device) override {}
  void audioDeviceStopped() override {}

  void audioDeviceError(const String& errorMessage) override {
    LOG(ERROR) << "Error on device " << id().first
               << ": " << errorMessage.toStdString();
  }

  void addCallback(InputCallback* cb) {
    ScopedLock l(lock_);
    callbacks_.push_back(std::move(cb));
  }

  void removeCallback(InputCallback* cb) {
    ScopedLock l(lock_);
    for (auto i = callbacks_.begin(); i != callbacks_.end(); ++i) {
      if (*i == cb) {
        callbacks_.erase(i);
        return;
      }
    }
  }

  const InputID& id() const override { return id_; }

 private:
  const InputID id_;
  AudioDeviceManager manager_;
  std::vector<InputCallback*> callbacks_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(InputImpl);
};

struct InputDeleter {
  void operator()(Input* base) {
    if (base) {
      ScopedLock l(INPUT_LOCK);
      INPUT_TABLE.erase(base->id());
      delete base;
    }
  }
};

}  // namespace

shared_ptr<Input> getInput(const string& name, int channels) {
  shared_ptr<Input> result(nullptr, InputDeleter());
  ScopedLock l(INPUT_LOCK);

  InputID id(name, channels);
  auto i = INPUT_TABLE.find(id);
  if (i != INPUT_TABLE.end()) {
    result.reset(i->second);
  } else {
    auto input = new InputImpl(id);
    result.reset(input);

    String error = input->initialize();
    if (error.length()) {
      LOG(DFATAL) << "Couldn't initialize input " << name;
      result.reset();
    } else {
      INPUT_TABLE[id] = input;
    }
  }
  return std::move(result);
}

}  // namespace audio
}  // namespace echomesh

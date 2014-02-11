#include "echomesh/audio/Input.h"
#include "echomesh/util/STL.h"

using namespace std;

namespace echomesh {
namespace audio {

#if 0
typedef tuple<bool, string, int> DeviceID;

struct Device {
  unique_ptr<AudioDeviceManager> manager_;
  int referenceCount_;
};

typedef map<DeviceID, Device> DeviceTable;

CriticalSection DEVICE_LOCK;
static DeviceTable DEVICE_TABLE;

struct DeviceDeleter {
  void operator()(AudioDeviceManager*);
};

typedef unique_ptr<AudioDeviceManager, DeviceDeleter> AudioDeviceManagerPointer;

AudioDeviceManagerPointer getDevice(
    bool isInput, const string& name = "", int channels = 2);

void DeviceDeleter::operator()(AudioDeviceManager* dm) {
  ScopedLock l(DEVICE_LOCK);
  for (auto& i: DEVICE_TABLE) {
    auto& device = i.second;
    if (device.manager_.get() == dm) {
      if (not --device.referenceCount_)
        DEVICE_TABLE.erase(i.first);
      return;
    }
  }
}

AudioDeviceManagerPointer getDevice(
    bool isInput, const string& name, int channels) {
  ScopedLock l(DEVICE_LOCK);

  AudioDeviceManagerPointer result;
  DeviceID id(isInput, name, channels);
  auto i = DEVICE_TABLE.find(id);
  if (i != DEVICE_TABLE.end()) {
    auto& device = i->second;
    device.referenceCount_++;
    result.reset(device.manager_.get());
  } else {
    Device device;
    device.referenceCount_ = 1;
    device.manager_ = make_unique<AudioDeviceManager>();
    String error = device.manager_->initialise(
        isInput ? channels : 0, isInput ? 0 : channels,
        nullptr, false, name);

    if (error.length()) {
      LOG(DFATAL) << "Couldn't initialize " << name << " for "
                  << (isInput ? "input." : "output.");
    } else {
      result.reset(device.manager_.get());
      DEVICE_TABLE[id] = move(device);
    }
  }
  return result;
}

#endif

unique_ptr<InputBase> getInput(const string& name, int channels) {
  unique_ptr<InputBase> result;
  return std::move(result);
}

class Input : public AudioIODeviceCallback {
 public:
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

  void addCallback(unique_ptr<InputCallback>);
  void removeCallback(InputCallback*);

 private:
  string name_;
  AudioDeviceManager manager_;
  std::vector<unique_ptr<InputCallback>> callbacks_;
  CriticalSection lock_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Input);
};

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

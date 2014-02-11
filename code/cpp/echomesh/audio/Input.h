#pragma once

#include "echomesh/audio/InputCallback.h"

namespace echomesh {
namespace audio {

class InputBase {
 public:
  virtual ~InputBase() {}
  virtual void addCallback(unique_ptr<InputCallback>) = 0;
  virtual void removeCallback(InputCallback*) = 0;
};

unique_ptr<InputBase> getInput(const string& name, int channels);

}  // namespace audio
}  // namespace echomesh

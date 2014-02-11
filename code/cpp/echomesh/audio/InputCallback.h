#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

class Input;

class InputCallback {
 public:
  virtual ~InputCallback() {}
  virtual void callback(int channels, int count, const float** samples) = 0;
};

}  // namespace audio
}  // namespace echomesh

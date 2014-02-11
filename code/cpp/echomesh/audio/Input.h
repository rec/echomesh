#pragma once

#include <memory>
#include "echomesh/audio/InputCallback.h"

namespace echomesh {
namespace audio {

typedef std::pair<string, int> InputID;

class Input {
 public:
  virtual ~Input() {}
  virtual void addCallback(InputCallback*) = 0;
  virtual void removeCallback(InputCallback*) = 0;
  virtual const InputID& id() const = 0;
};

std::shared_ptr<Input> getInput(const string& name, int channels);

}  // namespace audio
}  // namespace echomesh

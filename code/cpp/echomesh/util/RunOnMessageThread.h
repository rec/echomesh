#pragma once

#include <functional>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef std::function<void()> VoidFunction;

template <class Callback>
class RunOnMessageThread : public CallbackMessage {
  public:
    RunOnMessageThread(Callback f) : callback_(f) {}
    virtual void messageCallback() { callback_(); }
    Callback callback_;
};

template <class Callback>
void runOnMessageThread(Callback cb) {
    (new RunOnMessageThread<Callback>(cb))->post();
}

}  // namespace echomesh

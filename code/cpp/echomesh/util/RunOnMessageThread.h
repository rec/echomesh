#pragma once

#include <functional>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef std::function<void()> VoidFunction;

class RunOnMessageThread : public CallbackMessage {
 public:
  RunOnMessageThread(VoidFunction f) : function_(f) {}
  virtual void messageCallback() { function_(); }
  VoidFunction const function_;
};

inline void runOnMessageThread(VoidFunction f) {
  (new RunOnMessageThread(f))->post();
}

template <typename F, typename X>
void runOnMessageThread(F f, X x) {
  runOnMessageThread(std::bind(f, x));
}

template <typename F, typename X, typename Y>
void runOnMessageThread(F f, X x, Y y) {
  runOnMessageThread(std::bind(f, x, y));
}

}  // namespace echomesh


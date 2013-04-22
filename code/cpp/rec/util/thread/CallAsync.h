#ifndef __REC_UTIL_THREAD_CALLASYNC__
#define __REC_UTIL_THREAD_CALLASYNC__

#include "rec/util/thread/MakeCallback.h"

namespace rec {
namespace util {
namespace thread {
namespace callback {

class CallbackMessage : public juce::CallbackMessage,
                        public OwnedPointer<Callback> {
 public:
  CallbackMessage(Callback* r) : OwnedPointer<Callback>(r) {}
  virtual void messageCallback() {
  	(*this)();
  }
};

}  // namespace callback

inline void callAsync(Callback* cb) {
  (new thread::callback::CallbackMessage(cb))->post();
}

template <typename Type>
void callAsync(Type o) {
  callAsync(makeCallback<Type>(o));
}

template <typename Type, typename Method>
void callAsync(Type* o, Method m) {
  callAsync(methodCallback<Type, Method>(o, m));
}

template <typename Type, typename Method, typename Value>
void callAsync(Type* o, Method m, Value v) {
  callAsync(methodCallback<Type, Method, Value>(o, m, v));
}

template <typename Type, typename Method, typename V1, typename V2>
void callAsync(Type* o, Method m, V1 v1, V2 v2) {
  callAsync(methodCallback<Type, Method, V1, V2>(o, m, v1, v2));
}

}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_CALLASYNC__

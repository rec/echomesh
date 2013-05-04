#ifndef __REC_UTIL_THREAD_LOCKEDCALLBACK__
#define __REC_UTIL_THREAD_LOCKEDCALLBACK__

#include "rec/util/thread/MakeCallback.h"

namespace rec {
namespace util {
namespace thread {

class LockedCallback : public Callback {
 public:
  explicit LockedCallback(Callback *cb) : callback_(cb) {}

  virtual bool operator()() {
    MessageManagerLock l;
    return (*callback_)();
  }

 private:
  ptr<Callback> callback_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(LockedCallback);
};

template <typename Type>
Callback* lockedMakeCallback(Type o) {
  return new LockedCallback(makeCallback(o));
}

template <typename Type, typename Method>
Callback* lockedMethodCallback(Type* o, Method m) {
  return new LockedCallback(methodCallback(o, m));
}

template <typename Type, typename Method, typename Value>
Callback* lockedMethodCallback(Type* o, Method m, Value v) {
  return new LockedCallback(methodCallback(o, m, v));
}

template <typename Type, typename Method, typename V1, typename V2>
Callback* lockedMethodCallback(Type* o, Method m, V1 v1, V2 v2) {
  return new LockedCallback(methodCallback(o, m, v1, v2));
}

template <typename Type, typename Method, typename V1, typename V2, typename V3>
Callback* lockedMethodCallback(Type* o, Method m, V1 v1, V2 v2, V3 v3) {
  return new LockedCallback(methodCallback(o, m, v1, v2, v3));
}

template <typename Type, typename Method, typename V1, typename V2, typename V3, typename V4>
Callback* lockedMethodCallback(Type* o, Method m, V1 v1, V2 v2, V3 v3, V4 v4) {
  return new LockedCallback(methodCallback(o, m, v1, v2, v3, v4));
}

}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_LOCKEDCALLBACK__

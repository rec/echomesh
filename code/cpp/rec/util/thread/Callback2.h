#ifndef __REC_UTIL_THREAD_CALLBACK2__
#define __REC_UTIL_THREAD_CALLBACK2__

#include "rec/util/thread/Callback.h"

namespace rec {
namespace util {
namespace thread {
namespace callback {

template <typename Type, typename Method, typename V1, typename V2>
class Callback2 : public Callback {
 public:
  Callback2(Type* o, Method m, V1 v1, V2 v2) : object_(o), method_(m), v1_(v1), v2_(v2) {}
  virtual bool operator()() {
    (object_->*method_)(v1_, v2_);
    return true;
  }

 private:
  Type* object_;
  Method method_;
  V1 v1_;
  V2 v2_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Callback2);
};

template <typename Functor, typename V1, typename V2>
class CallbackFunc2 : public Callback {
 public:
  CallbackFunc2(Functor f, V1 v1, V2 v2) : functor_(f), v1_(v1), v2_(v2) {
  }

  virtual bool operator()() { (*functor_)(v1_, v2_); return true; }

 private:
  Functor functor_;
  V1 v1_;
  V2 v2_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackFunc2);
};

}  // namespace callback
}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_CALLBACK2__

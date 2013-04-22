#ifndef __REC_UTIL_THREAD_CALLBACK3__
#define __REC_UTIL_THREAD_CALLBACK3__

#include "rec/util/thread/Callback.h"

namespace rec {
namespace util {
namespace thread {
namespace callback {

template <typename Type, typename Method, typename V1, typename V2, typename V3>
class Callback3: public Callback {
 public:
  Callback3(Type* o, Method m, V1 v1, V2 v2, V3 v3) : object_(o), method_(m), v1_(v1), v2_(v2), v3_(v3) {}
  virtual bool operator()() {
    (object_->*method_)(v1_, v2_, v3_);
    return true;
  }

 private:
  Type* object_;
  Method method_;
  V1 v1_;
  V2 v2_;
  V3 v3_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Callback3);
};

template <typename Functor, typename V1, typename V2, typename V3>
class CallbackFunc3 : public Callback {
 public:
  CallbackFunc3(Functor f, V1 v1, V2 v2, V3 v3) : functor_(f), v1_(v1), v2_(v2), v3_(v3) {
  }

  virtual bool operator()() { (*functor_)(v1_, v2_, v3_); return true; }

 private:
  Functor functor_;
  V1 v1_;
  V2 v2_;
  V3 v3_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackFunc3);
};

}  // namespace callback
}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_CALLBACK3__

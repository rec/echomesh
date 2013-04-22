#ifndef __REC_UTIL_THREAD_CALLBACK4__
#define __REC_UTIL_THREAD_CALLBACK4__

#include "rec/util/thread/Callback.h"

namespace rec {
namespace util {
namespace thread {
namespace callback {

template <typename Type, typename Method, typename V1, typename V2, typename V3, typename V4>
class Callback4: public Callback {
 public:
  Callback4(Type* o, Method m, V1 v1, V2 v2, V3 v3, V4 v4) : object_(o), method_(m), v1_(v1), v2_(v2), v3_(v3), v4_(v4) {}
  virtual bool operator()() {
    (object_->*method_)(v1_, v2_, v3_, v4_);
    return true;
  }

 private:
  Type* object_;
  Method method_;
  V1 v1_;
  V2 v2_;
  V3 v3_;
  V4 v4_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Callback4);
};

template <typename Functor, typename V1, typename V2, typename V3, typename V4>
class CallbackFunc4 : public Callback {
 public:
  CallbackFunc4(Functor f, V1 v1, V2 v2, V3 v3, V4 v4) : functor_(f), v1_(v1), v2_(v2), v3_(v3), v4_(v4) {
  }

  virtual bool operator()() { (*functor_)(v1_, v2_, v3_, v4_); return true; }

 private:
  Functor functor_;
  V1 v1_;
  V2 v2_;
  V3 v3_;
  V4 v4_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackFunc4);
};

}  // namespace callback
}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_CALLBACK4__

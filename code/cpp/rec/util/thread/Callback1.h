#ifndef __REC_UTIL_THREAD_CALLBACK1__
#define __REC_UTIL_THREAD_CALLBACK1__

#include "rec/util/thread/Callback.h"

namespace rec {
namespace util {
namespace thread {
namespace callback {

template <typename Type, typename Method, typename Value>
class Callback1 : public Callback {
 public:
  Callback1(Type* o, Method m, Value v) : object_(o), method_(m), value_(v) {}

  virtual bool operator()() {
    (object_->*method_)(value_);
    return true;
  }

 private:
  Type* object_;
  Method method_;
  Value value_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Callback1);
};

template <typename Type, typename Method, typename Value>
class CallbackBool1 : public Callback {
 public:
  CallbackBool1(Type* o, Method m, Value v)
      : object_(o), method_(m), value_(v) {
  }

  virtual bool operator()() { return (object_->*method_)(); }

 private:
  Type* object_;
  Method method_;
  Value value_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackBool1);
};

template <typename Functor, typename Value>
class CallbackFunc1 : public Callback {
 public:
  CallbackFunc1(Functor f, Value v) : functor_(f), value_(v) {}

  virtual bool operator()() { (*functor_)(value_); return true; }

 private:
  Functor functor_;
  Value value_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CallbackFunc1);
};

}  // namespace callback
}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_CALLBACK1__

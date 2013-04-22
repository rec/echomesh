#ifndef __REC_UTIL_THREAD_MAKECALLBACK__
#define __REC_UTIL_THREAD_MAKECALLBACK__

#include "rec/util/thread/Callback0.h"
#include "rec/util/thread/Callback1.h"
#include "rec/util/thread/Callback2.h"
#include "rec/util/thread/Callback3.h"
#include "rec/util/thread/Callback4.h"
#include "rec/util/thread/Pointer.h"

namespace rec {
namespace util {
namespace thread {

// Callbacks for functions or methods which return null.

template <typename Type>
Callback* makeCallback(Type o) {
  return new callback::Pointer<Type>(o);
}

template <typename Type, typename Method>
Callback* methodCallback(Type* o, Method m) {
  return new callback::Callback0<Type, Method>(o, m);
}

template <typename Type, typename Method, typename Value>
Callback* methodCallback(Type* o, Method m, Value v) {
  return new callback::Callback1<Type, Method, Value>(o, m, v);
}

template <typename Type, typename Method, typename V1, typename V2>
Callback* methodCallback(Type* o, Method m, V1 v1, V2 v2) {
  return new callback::Callback2<Type, Method, V1, V2>(o, m, v1, v2);
}

template <typename Type, typename Method, typename V1, typename V2, typename V3>
Callback* methodCallback(Type* o, Method m, V1 v1, V2 v2, V3 v3) {
  return new callback::Callback3<Type, Method, V1, V2, V3>(o, m, v1, v2, v3);
}

template <typename Type, typename Method, typename V1, typename V2, typename V3, typename V4>
Callback* methodCallback(Type* o, Method m, V1 v1, V2 v2, V3 v3, V4 v4) {
  return new callback::Callback4<Type, Method, V1, V2, V3, V4>(o, m, v1, v2, v3, v4);
}

}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_MAKECALLBACK__

#ifndef __REC_UTIL_THREAD_FUNCTIONCALLBACK__
#define __REC_UTIL_THREAD_FUNCTIONCALLBACK__

#include "rec/util/thread/Callback.h"
#include "rec/util/thread/Callback1.h"
#include "rec/util/thread/Callback2.h"
#include "rec/util/thread/Callback3.h"
#include "rec/util/thread/Callback4.h"
#include "rec/util/thread/MakeCallback.h"

namespace rec {
namespace util {
namespace thread {

template <typename Type>
Callback* functionCB(Type o) {
  return makeCallback(o);
}

template <typename Function, typename Value>
Callback* functionCB(Function f, Value v) {
  return new callback::CallbackFunc1<Function, Value>(f, v);
}

template <typename Function, typename V1, typename V2>
Callback* functionCB(Function f, V1 v1, V2 v2) {
  return new callback::CallbackFunc2<Function, V1, V2>(f, v1, v2);
}

template <typename Function, typename V1, typename V2, typename V3>
Callback* functionCB(Function f, V1 v1, V2 v2, V3 v3) {
  return new callback::CallbackFunc3<Function, V1, V2, V3>(f, v1, v2, v3);
}

template <typename Function, typename V1, typename V2, typename V3, typename V4>
Callback* functionCB(Function f, V1 v1, V2 v2, V3 v3, V4 v4) {
  return new callback::CallbackFunc4<Function, V1, V2, V3, V4>(f, v1, v2, v3, v4);
}

}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_FUNCTIONCALLBACK__

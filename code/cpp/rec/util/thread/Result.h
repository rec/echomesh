#ifndef __REC_UTIL_THREAD_RESULT__
#define __REC_UTIL_THREAD_RESULT__

#include "rec/base/base.h"

namespace rec {
namespace util {
namespace thread {

enum Result {
  CONTINUE = -4,
  YIELD = -3,
  DONE = -2,
  WAIT = -1  // Everything from -1 on is a wait.
};

}  // namespace thread
}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_RESULT__

#ifndef __REC_UTIL_DELETABLE__
#define __REC_UTIL_DELETABLE__

#include "rec/base/base.h"

// A class with only a virtual destructor.

namespace rec {
namespace util {

class Deletable {
 public:
  Deletable() {}
  virtual ~Deletable() {}

 private:
  DISALLOW_COPY_ASSIGN_AND_LEAKS(Deletable);
};

}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_DELETABLE__

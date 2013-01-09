#include "Base.h"

namespace echomesh {

void dcheck(bool condition, const char* condName, const char* reason) {
  if (!condition) {
    if (reason)
      std::cerr << "Condition " << condition << " failed: " << reason;
    else
      std::cerr << "Condition " << condition << " failed";
  }
}

}  // namespace echomesh

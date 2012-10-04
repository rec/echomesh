#include "Base.h"

namespace echomesh {

void dcheck(bool condition, const char* message) {
  if (!condition)
    std::cerr << "Condition " << message << " failed";
}

}  // namespace echomesh

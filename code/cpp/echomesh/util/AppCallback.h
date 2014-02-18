#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef void (*VoidCaller)(void *callback);
typedef void (*StringCaller)(void *callback, string data);

}  // namespace echomesh


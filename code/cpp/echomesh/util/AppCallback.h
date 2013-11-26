#ifndef __ECHOMESH_APPCALLBACK__
#define __ECHOMESH_APPCALLBACK__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef void (*VoidCaller)(void *callback);
typedef void (*StringCaller)(void *callback, string data);

}  // namespace echomesh

#endif  // __ECHOMESH_APPCALLBACK__

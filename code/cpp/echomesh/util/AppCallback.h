#ifndef __ECHOMESH_APPCALLBACK__
#define __ECHOMESH_APPCALLBACK__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef void (*AppCallback)(void *callback);
typedef void (*StringCallback)(void *callback, string data);

}  // namespace echomesh

#endif  // __ECHOMESH_APPCALLBACK__

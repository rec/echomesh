#ifndef __ECHOMESH_ECHOMESHAPPLICATION__
#define __ECHOMESH_ECHOMESHAPPLICATION__

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(AppCallback cb, void* userData);
void stopApplication();

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESHAPPLICATION__

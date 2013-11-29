#ifndef __ECHOMESH_ECHOMESHAPPLICATION__
#define __ECHOMESH_ECHOMESHAPPLICATION__

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(VoidCaller, void*);
void stopApplication();
bool isStarted();

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESHAPPLICATION__

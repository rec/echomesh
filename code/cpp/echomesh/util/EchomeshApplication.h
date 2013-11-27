#ifndef __ECHOMESH_ECHOMESHAPPLICATION__
#define __ECHOMESH_ECHOMESHAPPLICATION__

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(VoidCaller, void*);
void stopApplication();
void write(const string&);
void flush();
void readConsole(StringCaller, void*);

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESHAPPLICATION__

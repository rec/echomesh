#ifndef __ECHOMESH_ECHOMESHAPPLICATION__
#define __ECHOMESH_ECHOMESHAPPLICATION__

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(VoidCaller, void*);
void stopApplication();
void cprint(const string&);
void cflush();
void readConsole(StringCaller, void*);
void setConsolePrompt(const string&);

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESHAPPLICATION__

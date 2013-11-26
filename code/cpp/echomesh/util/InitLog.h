#ifndef __ECHOMESH_INITLOG__
#define __ECHOMESH_INITLOG__

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void initLog();
void setLogger(int logLevel, StringCaller, void* callback);

}  // namespace echomesh

#endif  // __ECHOMESH_INITLOG__

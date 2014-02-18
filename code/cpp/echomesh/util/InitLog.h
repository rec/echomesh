#pragma once

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void initLog();
void setLogger(int logLevel, StringCaller, void* callback);

}  // namespace echomesh


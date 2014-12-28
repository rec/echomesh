#pragma once

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(StringCaller, void*);
bool isStarted();

string timestamp();
string datestamp();

}  // namespace echomesh

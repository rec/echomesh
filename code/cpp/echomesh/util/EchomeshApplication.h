#pragma once

#include "echomesh/util/AppCallback.h"

namespace echomesh {

void startApplication(VoidCaller, void*);
bool isStarted();

string timestamp();
string datestamp();

}  // namespace echomesh

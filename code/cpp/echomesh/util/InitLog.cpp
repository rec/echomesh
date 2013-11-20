#include "echomesh/util/InitLog.h"

namespace echomesh {

namespace {

bool initialized = false;

}  // namespace

void initLog() {
  if (not initialized) {
    initialized = true;
    google::InitGoogleLogging("echomesh");
    FLAGS_logtostderr = true;
  }
}

}  // namespace echomesh

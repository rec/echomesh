#include "echomesh/util/InitLog.h"

namespace echomesh {

namespace {

struct Initializer {
  Initializer() {
    google::InitGoogleLogging(name());
    FLAGS_logtostderr = true;
  }

  const char* name() const { return "echomesh"; }
};

}  // namespace

const char* initLog() {
  static Initializer initializer;
  return initializer.name();
}

}  // namespace echomesh

#include "echomesh/util/InitLog.h"

namespace echomesh {

namespace {

struct Initializer {
  Initializer() {
    google::InitGoogleLogging(name());
#if JUCE_DEBUG && JUCE_MAC
    FLAGS_logtostderr = true;
#endif
  }

  const char* name() const { return "echomesh"; }
};

}  // namespace

const char* initLog() {
  static Initializer initializer;
  return initializer.name();
}

}  // namespace echomesh

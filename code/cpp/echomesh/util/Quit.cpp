#include "echomesh/util/Quit.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {

void quit() {
    runOnMessageThread(JUCEApplicationBase::quit);
}

}  // namespace echomesh

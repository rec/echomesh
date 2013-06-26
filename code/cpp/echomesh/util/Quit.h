#ifndef __ECHOMESH_QUIT__
#define __ECHOMESH_QUIT__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct QuitMessage : public CallbackMessage {
  virtual void messageCallback() {
    JUCEApplication::quit();
  };
};

inline void quit() {
  (new QuitMessage)->post();
}

}  // namespace echomesh

#endif  // __ECHOMESH_QUIT__

#ifndef __ECHOMESH_ECHOMESH__
#define __ECHOMESH_ECHOMESH__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class LightingWindow;
class LightReader;
class Player;

class Echomesh {
 public:
  Echomesh() {}
  ~Echomesh();

  void initialise();
  void shutdown();

 private:
  ScopedPointer<LightingWindow> lightingWindow_;
  ScopedPointer<LightReader> readThread_;
  ScopedPointer<Player> player_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Echomesh);
};

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESH__

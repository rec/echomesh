#ifndef __ECHOMESH_RUNNABLE__
#define __ECHOMESH_RUNNABLE__

namespace echomesh {

class Runnable {
 public:
  Runnable() {}
  virtual ~Runnable() {}
  virtual bool isRunning() const = 0;
};

}  // namespace echomesh

#endif __ECHOMESH_RUNNABLE__

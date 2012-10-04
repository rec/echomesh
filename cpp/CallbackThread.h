#ifndef __ECHOMESH__CALLBACKTHREAD__
#define __ECHOMESH__CALLBACKTHREAD__

#include <pthread.h>

#include "Base.h"

namespace echomesh {

class Callback;

class CallbackThread {
 public:
  CallbackThread();
  ~CallbackThread();

  bool addCallback(Callback*);

 private:
  void start();

  Mutex mutex_;
  scoped_ptr<Callback> callback_;
  pthread_attr_t threadAttributes_;

  DISALLOW_COPY_AND_ASSIGN(CallbackThread);
};

}  // namespace echomesh

#endif  // __ECHOMESH__CALLBACKTHREAD__

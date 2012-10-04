#ifndef __ECHOMESH__CALLBACKTHREAD__
#define __ECHOMESH__CALLBACKTHREAD__

#include <pthread.h>
#include <signal.h>

#include "Base.h"

namespace echomesh {

class Callback;

class CallbackThread {
 public:
  CallbackThread();
  ~CallbackThread();

  bool addCallback(Callback*);
  void requestExit();
  bool isRunning() const;

 private:
  static void* runCallbackThread(void*);
  void run();

  mutable Mutex mutex_;
  scoped_ptr<Callback> callback_;
  pthread_attr_t threadAttributes_;
  pthread_t thread_;
  sigset_t signalMask_;
  bool exitRequested_;
  bool isRunning_;

  DISALLOW_COPY_AND_ASSIGN(CallbackThread);
};

}  // namespace echomesh

#endif  // __ECHOMESH__CALLBACKTHREAD__

#ifndef __ECHOMESH__CALLBACKTHREAD__
#define __ECHOMESH__CALLBACKTHREAD__

#include <pthread.h>
#include <signal.h>

#include "Base.h"

namespace echomesh {

class Callback;

// This class deletes itself when it finishes running.
class CallbackThread {
 public:
  CallbackThread(Callback* cb = NULL);
  ~CallbackThread();

  // Try to add a new callback to this thread.
  // Return true if successful, or false if the thread is currently running
  // a callback.
  bool addCallback(Callback*);
  bool hasCallback() const;

  // Ask for the thread to exit.
  void requestExit();
  bool isRunning() const;

 private:
  static void* runCallbackThread(void*);
  void run();
  void notify();
  void wait();

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

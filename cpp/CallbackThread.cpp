#include "CallbackThread.h"

#include "Callback.h"
#include "Lock.h"

namespace echomesh {

CallbackThread::CallbackThread() {
  pthread_attr_init(&threadAttributes_);
}

CallbackThread::~CallbackThread() {
  Lock l(&mutex_);
  DCHECK(!callback_);
  pthread_attr_destroy(&threadAttributes_);
}

bool CallbackThread::addCallback(Callback* cb) {
  Lock l(&mutex_);
  if (callback_)
    return false;
  callback_.reset(cb);
  return true;
}

void CallbackThread::start() {
}

}  // namespace echomesh

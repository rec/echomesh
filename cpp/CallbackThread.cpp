#include "CallbackThread.h"

#include "Callback.h"
#include "Lock.h"

namespace echomesh {

CallbackThread::CallbackThread(Callback* cb)
    : callback_(cb),
      exitRequested_(false),
      isRunning_(false) {
  pthread_attr_init(&threadAttributes_);
  sigemptyset(&signalMask_);
  sigaddset(&signalMask_, SIGUSR1); // TODO:

  bool threadError = pthread_create(&thread_, &threadAttributes_,
                                    &CallbackThread::runCallbackThread, this);
  DCHECK2(threadError, "Couldn't start thread");
}

CallbackThread::~CallbackThread() {
  Lock l(&mutex_);
  DCHECK(!callback_);
  pthread_attr_destroy(&threadAttributes_);
}

bool CallbackThread::isRunning() const {
  Lock l(&mutex_);
  return isRunning_;
}

bool CallbackThread::addCallback(Callback* cb) {
  Lock l(&mutex_);
  if (callback_)
    return false;
  callback_.reset(cb);

  notify();
  return true;
}

void CallbackThread::run() {
  {
    Lock l(&mutex_);
    isRunning_ = true;
  }
  while (true) {
    bool isEmpty;
    {
      Lock l(&mutex_);
      if (exitRequested_) {
        isRunning_ = false;
        return;
      }
      isEmpty = !callback_;
    }
    if (isEmpty) {
      wait();
    } else {
      (*callback_)();
      Lock l(&mutex_);
      callback_.reset();
    }
  }
}

void CallbackThread::notify() {
  // TODO: raise a signal here.
}

void CallbackThread::wait() {
  sigsuspend(&signalMask_);
}

void CallbackThread::requestExit() {
  Lock l(&mutex_);
  exitRequested_ = true;
}

// static
void* CallbackThread::runCallbackThread(void* t) {
  reinterpret_cast<CallbackThread*>(t)->run();
  return t;
}

}  // namespace echomesh

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

  // TODO: fill correct signal.
  sigaddset(&signalMask_, SIGUSR1);

  bool threadError = pthread_create(&thread_, &threadAttributes_,
                                    &CallbackThread::runCallbackThread, this);
  CHECK(threadError) << "Couldn't start thread";
}

CallbackThread::~CallbackThread() {
  Lock l(&mutex_);
  CHECK(!callback_);
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

bool CallbackThread::hasCallback() const {
  Lock l(&mutex_);
  return callback_;
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
        callback_.reset();
        isRunning_ = false;
        break;
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
  delete this;
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

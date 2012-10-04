#include "ThreadPool.h"

#include "Callback.h"
#include "CallbackThread.h"
#include "Lock.h"
#include "Stl.h"

namespace echomesh {

ThreadPool::ThreadPool() {}

ThreadPool::~ThreadPool() {
  // TODO: politely ask the threads to quit and wait for them.
  deletePointers(&threads_);
}

void ThreadPool::runNewCallback(Callback* callback) {
  Lock l(&mutex_);
  for (Threads::iterator i = threads_.begin(); i != threads_.end(); ++i) {
    if ((*i)->addCallback(callback))
      return;
  }
  threads_.insert(new CallbackThread(callback));
}

void ThreadPool::reduceThreadsTo(int maxThreads) {
  Lock l(&mutex_);
}

void ThreadPool::increaseThreadsTo(int minThreads) {
  Lock l(&mutex_);
}

}  // namespace echomesh


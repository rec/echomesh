#include "ThreadPool.h"

#include "Callback.h"
#include "CallbackThread.h"
#include "Lock.h"
#include "Stl.h"

namespace echomesh {

ThreadPool::ThreadPool() {}

ThreadPool::~ThreadPool() {
  for (Threads::iterator i = threads_.begin(); i != threads_.end(); ++i)
    (*i)->requestExit();
}

void ThreadPool::runNewCallback(Callback* callback) {
  Lock l(&mutex_);
  for (Threads::iterator i = threads_.begin(); i != threads_.end(); ++i) {
    if ((*i)->addCallback(callback))
      return;
  }
  threads_.insert(new CallbackThread(callback));
}

int ThreadPool::reduceThreadsTo(int maxThreads) {
  Lock l(&mutex_);
  uint toRemove = threads_.size() - maxThreads;
  if (toRemove > 0) {
    std::vector<CallbackThread*> removedThreads;
    for (Threads::iterator i = threads_.begin(); i != threads_.end(); ++i) {
      if (!(*i)->hasCallback()) {
        (*i)->requestExit();
        removedThreads.push_back(*i);
        if (removedThreads.size() >= toRemove)
          break;
      }
    }
    for (uint i = 0; i < removedThreads.size(); ++i)
      threads_.erase(removedThreads[i]);
  }
  return threads_.size();
}

int ThreadPool::increaseThreadsTo(int minThreads) {
  Lock l(&mutex_);
  int toAdd = minThreads - threads_.size();
  for (int i = 0; i < toAdd; ++i)
    threads_.insert(new CallbackThread);

  return threads_.size();
}

}  // namespace echomesh


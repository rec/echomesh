#ifndef __ECHOMESH__THREADPOOL__
#define __ECHOMESH__THREADPOOL__

#include <set>

#include "Base.h"

namespace echomesh {

class Callback;
class CallbackThread;

class ThreadPool {
 public:
  ThreadPool();
  ~ThreadPool();

  void runNewCallback(Callback*);
  void reduceThreadsTo(int);
  void increaseThreadsTo(int);

 private:
  typedef std::set<CallbackThread*> Threads;
  Threads threads_;
  Mutex mutex_;

  DISALLOW_COPY_AND_ASSIGN(ThreadPool);
};

}  // namespace echomesh

#endif  // __ECHOMESH__THREADPOOL__

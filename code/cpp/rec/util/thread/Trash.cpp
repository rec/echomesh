#include "rec/util/thread/Trash.h"

namespace rec {
namespace util {
namespace thread {
namespace trash {

namespace {

class Trash {
 public:
  Trash() {}

  ~Trash() {
    ScopedLock l(lock_);
    empty();
  }

  void add(Thread* thread) {
    ScopedLock l(lock_);
    threads_.insert(thread);
  }

  void doDelete(Thread* thread) {
    delete thread;
  }

  void discard(Thread* thread) {
    if (thread) {
      thread->signalThreadShouldExit();
      thread->notify();
      if (thread->isThreadRunning())
        add(thread);
      else
        doDelete(thread);
    }
  }

  void empty() {
    ThreadSet stopped;
    {
      ScopedLock l(lock_);
      for (ThreadSet::iterator i = threads_.begin(); i != threads_.end(); ++i) {
        if (!(*i)->isThreadRunning())
          stopped.insert(*i);
      }
      for (ThreadSet::iterator i = stopped.begin(); i != stopped.end(); ++i)
        threads_.erase(*i);
    }

    for (ThreadSet::iterator i = stopped.begin(); i != stopped.end(); ++i) {
      // LOG(DFATAL) << "Not deleting " << *i;
      doDelete(*i);
    }
  }

  void waitForAllThreadsToExit(int timeout) {
    ScopedLock l(lock_);
    empty();
    for (ThreadSet::iterator i = threads_.begin(); i != threads_.end(); ++i)
      (*i)->waitForThreadToExit(timeout);
    empty();
  }

 private:
  CriticalSection lock_;

  typedef std::set<Thread*> ThreadSet;
  ThreadSet threads_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Trash);
};

Trash* instance() {
  static Trash trash;
  return &trash;
}

}  // namespace

Thread* add(Thread* t) { instance()->add(t); return t; }
void run(Thread* t) { t->startThread(); instance()->add(t); }
void discard(Thread* t) { instance()->discard(t); }
void empty() { instance()->empty(); }
void waitForAllThreadsToExit(int t) { instance()->waitForAllThreadsToExit(t); }

}  // namespace trash
}  // namespace thread
}  // namespace util
}  // namespace rec

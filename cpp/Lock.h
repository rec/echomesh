#ifndef __ECHOMESH__LOCK__
#define __ECHOMESH__LOCK__

#include "Base.h"

namespace echomesh {

typedef pthread_mutex_t Mutex;

class Lock {
 public:
  Lock(Mutex* mutex) : mutex_(mutex) { pthread_mutex_lock(mutex_); }
  ~Lock() { pthread_mutex_unlock(mutex_); }

 private:
  Mutex* const mutex_;

  DISALLOW_COPY_ASSIGN_AND_EMPTY(Lock);
};

}  // namespace echomesh

#endif // __ECHOMESH__LOCK__

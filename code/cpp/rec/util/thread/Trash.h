#ifndef __REC_UTIL_THREAD_TRASH__
#define __REC_UTIL_THREAD_TRASH__

#include <set>

#include "rec/base/base.h"
#include "rec/util/STL.h"

namespace rec {
namespace util {
namespace thread {
namespace trash {

void discard(Thread* t);

template <typename ThreadClass>
void discard(ptr<ThreadClass>* t) {
  discard(t->transfer());
}

Thread* add(Thread* t);
void run(Thread *t);
template <typename T> void run() { run(new T); }


void empty();
void waitForAllThreadsToExit(int timeout);
inline void discardAndEmpty(Thread* t) { discard(t); empty(); }

}  // namespace trash
}  // namespace thread


template <typename Type>
class thread_ptr : public ptr<Type> {
public:
  explicit thread_ptr(Type* p = 0) : ptr<Type>(p) {}

  ~thread_ptr() { reset(); }

  void reset(Type* p = NULL) {
    if (p != this->get()) {
      thread::trash::discard(this->transfer());
      ptr<Type>::reset(p);
    }
  }

  operator bool() const { return this->get(); }
  bool operator!() const { return !this->get(); }

  DISALLOW_COPY_ASSIGN_AND_LEAKS(thread_ptr);
};

}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_THREAD_TRASH__

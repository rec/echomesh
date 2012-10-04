#ifndef __REC_THREAD_CALLBACK__
#define __REC_THREAD_CALLBACK__

#include "Base.h"

namespace echomesh {

class Callback {
 public:
  Callback() {}
  virtual ~Callback() {}

  virtual bool operator()() = 0;

 private:
  DISALLOW_COPY_AND_ASSIGN(Callback);
};

}  // namespace echomesh

#endif  // __REC_THREAD_CALLBACK__

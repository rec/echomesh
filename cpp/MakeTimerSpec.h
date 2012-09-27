#ifndef __ECHOMESH_MAKE_TIMER_SPEC__
#define __ECHOMESH_MAKE_TIMER_SPEC__

#include <time.h>
#include <string>

namespace echomesh {

itimerspec makeTimerSpec(const std::string&);

}  // namespace echomesh

#endif  // __ECHOMESH_MAKE_TIMER_SPEC__

#ifndef __REC_BASE_BASE__

#include <stdlib.h>
#include <stdio.h>

#include <iostream>
#include <string>

#include "ScopedPtr.h"

#include "Disallow.h"
#include "Types.h"

typedef pthread_mutex_t Mutex;

namespace echomesh {

void dcheck(bool condition, const char* condName, const char* reason);

}  // namespace echomesh

#define DCHECK(X) dcheck(X, #X, NULL)
#define DCHECK2(X, Y) dcheck(X, #X, Y)

#endif

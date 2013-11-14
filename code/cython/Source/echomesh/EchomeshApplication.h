#ifndef __ECHOMESH_ECHOMESHAPPLICATION__
#define __ECHOMESH_ECHOMESHAPPLICATION__

namespace echomesh {

typedef void (*AppCallback)(void *userData);

void startApplication(AppCallback cb, void* userData);
void stopApplication();

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESHAPPLICATION__

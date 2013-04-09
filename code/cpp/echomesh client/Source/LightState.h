#ifndef __ECHOMESH_LIGHT_STATE__
#define __ECHOMESH_LIGHT_STATE__

#include <vector>

namespace echomesh {

typedef unsigned char byte;

struct Light {
  byte r_, g_, b_;
};

typedef std::vector<Light> LightList;


}  // namespace echomesh

#endif __ECHOMESH_LIGHT_STATE__

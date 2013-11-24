#ifndef __ECHOMESH_GETREADER__
#define __ECHOMESH_GETREADER__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

unique_ptr<PositionableAudioSource> getReader(
    const String&, SampleTime begin, SampleTime end);

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_GETREADER__

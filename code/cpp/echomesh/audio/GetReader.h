#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

unique_ptr<PositionableAudioSource> getReader(
    const String&, SampleTime begin, SampleTime end, float sampleRate,
    int channels);

}  // namespace audio
}  // namespace echomesh


#ifndef __ECHOMESH_SOURCE__
#define __ECHOMESH_SOURCE__

#include "echomesh/audio/SampleAudioSource.h"
#include "echomesh/util/AppCallback.h"

namespace echomesh {
namespace audio {

class AudioPlayer;

class Source : public SampleAudioSource {
 public:
  Source(const string& filename, int loops,
         double begin, double end, double length,
         const string& device, int channels,
         Envelope* gain, Envelope* pan, VoidCaller callback,
         void* callbackData, float sampleRate);

  ~Source();

 private:
  AudioPlayer* const player_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Source);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_SOURCE__

#ifndef __ECHOMESH_SOURCE__
#define __ECHOMESH_SOURCE__

#include "echomesh/audio/SampleAudioSource.h"

namespace echomesh {
namespace audio {

class AudioPlayer;

class Source : public SampleAudioSource {
 public:
  Source(const string& filename, int loops,
         long long begin, long long end, long long length,
         const string& device, int channels,
         Envelope* gain, Envelope* pan);

  ~Source();

 private:
  AudioPlayer* const player_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(Source);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_SOURCE__

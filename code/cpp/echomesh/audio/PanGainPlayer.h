#ifndef __ECHOMESH_AUDIO_PANGAINPLAYER__
#define __ECHOMESH_AUDIO_PANGAINPLAYER__

#include "echomesh/audio/Envelope.h"
#include "echomesh/audio/EnvelopePlayer.h"

namespace echomesh {
namespace audio {

class PanGainPlayer {
 public:
  PanGainPlayer(const Envelope& gain, const Envelope& pan, bool passthrough)
      : gainPlayer_(gain), panPlayer_(pan), passthrough_(passthrough) {
  }

  void apply(const AudioSourceChannelInfo&);
  void begin();

 private:
  EnvelopePlayer gainPlayer_, panPlayer_;
  bool passthrough_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(PanGainPlayer);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_PANGAINPLAYER__

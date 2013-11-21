#ifndef __ECHOMESH_AUDIO_PANGAINPLAYER__
#define __ECHOMESH_AUDIO_PANGAINPLAYER__

#include "echomesh/audio/Envelope.h"
#include "echomesh/audio/EnvelopePlayer.h"

namespace echomesh {
namespace audio {

class PanGainPlayer {
 public:
  PanGainPlayer(Envelope* gain, Envelope* pan, bool passthrough);

  void apply(const AudioSourceChannelInfo&);
  void begin();

 private:
  void applyGain(const AudioSourceChannelInfo&);
  void applyPan(const AudioSourceChannelInfo&);

  unique_ptr<EnvelopePlayer> gainPlayer_, panPlayer_;
  bool passthrough_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(PanGainPlayer);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_PANGAINPLAYER__

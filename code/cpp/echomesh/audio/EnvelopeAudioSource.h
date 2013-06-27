#ifndef __ECHOMESH_ENVELOPEAUDIOSOURCE__
#define __ECHOMESH_ENVELOPEAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"

namespace YAML { class Node; }

namespace echomesh {

class EnvelopeAudioSource : public AudioSource {
 public:
  EnvelopeAudioSource(const YAML::Node&);
  virtual ~EnvelopeAudioSource();

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);

  virtual void releaseResources();
  virtual void getNextAudioBlock (const AudioSourceChannelInfo& bufferToFill);

  void run();
  void begin();
  void pause();
  void unload();

 private:


  DISALLOW_COPY_ASSIGN_AND_LEAKS(EnvelopeAudioSource);
};

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPEAUDIOSOURCE__

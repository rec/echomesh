#ifndef __ECHOMESH_SAMPLEAUDIOSOURCE__
#define __ECHOMESH_SAMPLEAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class SampleAudioSource : public AudioSource {
 public:
  SampleAudioSource(const Node&);
  virtual ~SampleAudioSource();

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);

  virtual void releaseResources();
  virtual void getNextAudioBlock (const AudioSourceChannelInfo& bufferToFill);

  void run();
  void begin();
  void pause();
  void unload();

 private:
  DISALLOW_COPY_ASSIGN_AND_LEAKS(SampleAudioSource);
};

#endif  // __ECHOMESH_SAMPLEAUDIOSOURCE__
}  // namespace echomesh


#ifndef __ECHOMESH_SAMPLEAUDIOSOURCE__
#define __ECHOMESH_SAMPLEAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

class SampleAudioSource : public AudioSource {
 public:
  SampleAudioSource(const Node&);
  virtual ~SampleAudioSource();

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);

  virtual void releaseResources();
  virtual void getNextAudioBlock(const AudioSourceChannelInfo&);

  void run();
  void begin();
  void pause();
  void unload();

 private:
  CriticalSection lock_;

  Playback playback_;
  SampleTime currentTime_;
  SampleTime length_;
  ScopedPointer<PositionableAudioSource> source_;
  bool isRunning_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(SampleAudioSource);
};

}  // namespace echomesh

#endif  // __ECHOMESH_SAMPLEAUDIOSOURCE__

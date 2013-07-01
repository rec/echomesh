#ifndef __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__
#define __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class PlaybackAudioSource : public AudioSource {
 public:
  PlaybackAudioSource() {}

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);
  virtual void releaseResources() {}

  virtual void getNextAudioBlock(const AudioSourceChannelInfo&);
  void addSource(AudioSource*);
  void removeSource(AudioSource*);

 private:
  AudioSourceChannelInfo info_;
  ScopedPointer<AudioSampleBuffer> buffer_;

  typedef OwnedArray<AudioSource> SourceArray;
  SourceArray sources_;
  CriticalSection lock_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PlaybackAudioSource)
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

#ifndef __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__
#define __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class PlaybackAudioSource : public AudioSource {
 public:
  PlaybackAudioSource() {}

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double /*sampleRate*/) {
    if (buffer_)
      buffer_->setSize(2, samplesPerBlockExpected, false, false, true);
    else
      buffer_ = new AudioSampleBuffer(2, samplesPerBlockExpected);
    info_.numSamples = samplesPerBlockExpected;
    info_.buffer = buffer_;
  }

  virtual void releaseResources() {}

  virtual void getNextAudioBlock(const AudioSourceChannelInfo& block) {
    ScopedLock l(lock_);

    if (not sources_.size()) {
      block.clearActiveBufferRegion();
      return;
    }
    sources_[0]->getNextAudioBlock(block);
    if (sources_.size() == 1)
      return;

    prepareToPlay(block.numSamples, 44100.0);
    for (int i = 1; i < sources_.size(); ++i) {
      sources_[i]->getNextAudioBlock(info_);
      for (int ch = 0; ch < 2; ++ch)
        block.buffer->addFrom(ch, 0, *info_.buffer, 0, 0, block.numSamples);
    }
  }

 private:
  AudioSourceChannelInfo info_;
  ScopedPointer<AudioSampleBuffer> buffer_;

  typedef OwnedArray<PositionableAudioSource> SourceArray;
  SourceArray sources_;
  CriticalSection lock_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PlaybackAudioSource)
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_PLAYBACKAUDIOSOURCE__

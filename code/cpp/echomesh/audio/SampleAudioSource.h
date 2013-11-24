#ifndef __ECHOMESH_SAMPLEAUDIOSOURCE__
#define __ECHOMESH_SAMPLEAUDIOSOURCE__

#include "echomesh/audio/PanGainPlayer.h"
#include "echomesh/util/AppCallback.h"

namespace echomesh {
namespace audio {

class SampleAudioSource : public AudioSource {
 public:
  explicit SampleAudioSource(const Node&);

  SampleAudioSource(const String& filename, int loops,
                    SampleTime begin, SampleTime end, SampleTime length,
                    Envelope* gain, Envelope* pan, AppCallback callback,
                    void* callbackData, float sampleRate, int channels);

  virtual ~SampleAudioSource();

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);

  virtual void releaseResources();
  virtual void getNextAudioBlock(const AudioSourceChannelInfo&);

  const string& error() const { return error_; }

  void run();
  void begin();
  void pause();

 private:
  void init(const String& filename, int loops,
            SampleTime begin, SampleTime end, SampleTime length,
            Envelope* gain, Envelope* pan, float sampleRate, int channels);

  CriticalSection lock_;

  SampleTime currentTime_;
  SampleTime length_;
  unique_ptr<PositionableAudioSource> source_;
  bool isRunning_;
  string error_;

  Envelope* gain_;
  Envelope* pan_;
  unique_ptr<PanGainPlayer> panGainPlayer_;
  AppCallback const callback_;
  void* const callbackData_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(SampleAudioSource);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_SAMPLEAUDIOSOURCE__

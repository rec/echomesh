#ifndef __ECHOMESH_SAMPLEAUDIOSOURCE__
#define __ECHOMESH_SAMPLEAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"
#include "echomesh/audio/PanGainPlayer.h"

namespace echomesh {
namespace audio {

class SampleAudioSource : public AudioSource {
 public:
  explicit SampleAudioSource(const Node&);

  SampleAudioSource(const String& filename, int loops,
                    SampleTime begin, SampleTime end, SampleTime length,
                    Envelope* gain, Envelope* pan);

  virtual ~SampleAudioSource();

  virtual void prepareToPlay(int samplesPerBlockExpected,
                             double sampleRate);

  virtual void releaseResources();
  virtual void getNextAudioBlock(const AudioSourceChannelInfo&);

  const string& error() const { return error_; }

  void run();
  void begin();
  void pause();
  void unload();

 private:
  void init(const String& filename, int loops,
            SampleTime begin, SampleTime end, SampleTime length,
            Envelope* gain, Envelope* pan);

  CriticalSection lock_;

  SampleTime currentTime_;
  SampleTime length_;
  unique_ptr<PositionableAudioSource> source_;
  bool isRunning_;
  string error_;

  unique_ptr<Envelope> gain_, pan_;

  unique_ptr<PanGainPlayer> panGainPlayer_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(SampleAudioSource);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_SAMPLEAUDIOSOURCE__

#ifndef __ECHOMESH_SAMPLEAUDIOSOURCE__
#define __ECHOMESH_SAMPLEAUDIOSOURCE__

#include "echomesh/base/Echomesh.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

class SampleAudioSource : public AudioSource {
 public:
  explicit SampleAudioSource(const Node&);
  SampleAudioSource(const String& filename, int loops,
                    SampleTime begin, SampleTime end, SampleTime length) {
    std::cerr << "SampleAudioSource\n";
    init(filename, loops, begin, end, length);
  }

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
  void init(const String& filename, int loops,
            SampleTime begin, SampleTime end, SampleTime length);

  CriticalSection lock_;

  SampleTime currentTime_;
  SampleTime length_;
  unique_ptr<PositionableAudioSource> source_;
  bool isRunning_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(SampleAudioSource);
};

}  // namespace echomesh

#endif  // __ECHOMESH_SAMPLEAUDIOSOURCE__

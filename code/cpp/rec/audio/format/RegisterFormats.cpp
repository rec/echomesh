#include "rec/audio/format/RegisterFormats.h"

#if REC_USE_MPG123
#include "rec/audio/format/mpg123/Format.h"
#endif

namespace rec {
namespace audio {
namespace format {

namespace {

using namespace juce;

void registerSoftwareFormats(AudioFormatManager* afm, ReadWrite rw) {
  afm->registerFormat(new WavAudioFormat, true);
  afm->registerFormat(new AiffAudioFormat, false);
}

void registerOptionalFormats(AudioFormatManager* afm) {
#if JUCE_USE_FLAC
  afm->registerFormat(new FlacAudioFormat, false);
#endif

#if JUCE_USE_OGGVORBIS
  afm->registerFormat(new OggVorbisAudioFormat, false);
#endif
}

}  // namespace

void registerFormats(AudioFormatManager* afm, ReadWrite rw) {
#if REC_USE_MPG123
  afm->registerFormat(new mpg123::Format, false);
#endif

#if (JUCE_MAC || JUCE_IOS)
  if (rw == READ || JUCE_USE_COREAUDIO_WRITE)
    afm->registerFormat(new CoreAudioFormat, false);
  else
    registerSoftwareFormats(afm, rw);

#elif JUCE_USE_WINDOWS_MEDIA_FORMAT
  registerSoftwareFormats(afm, rw);
  if (rw == READ || JUCE_USE_WINDOWSMEDIA_WRITE)
    afm->registerFormat(new WindowsMediaAudioFormat, false);
#endif

  registerOptionalFormats(afm);
}

AudioFormatManager* createAudioFormatManager(ReadWrite rw) {
  ScopedPointer<AudioFormatManager> afm(new AudioFormatManager);
  registerFormats(afm, rw);
  return afm.release();
}

}  // namespace format
}  // namespace audio
}  // namespace rec


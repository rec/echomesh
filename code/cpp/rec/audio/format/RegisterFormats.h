#ifndef __REC_AUDIO_REGISTERFORMATS__
#define __REC_AUDIO_REGISTERFORMATS__

#include "rec/base/base.h"

// Does Juce's MP3AudioFormat support writing?
static const bool JUCE_USE_MP3AUDIOFORMAT_WRITE = false;

// Does Juce's CoreAudioFormat support writing?
static const bool JUCE_USE_COREAUDIO_WRITE = false;

// Does Juce's WindowsMediaAudioFormat support writing?
static const bool JUCE_USE_WINDOWSMEDIA_WRITE = false;

#ifndef REC_USE_MPG123
#define REC_USE_MPG123 0
#endif

namespace rec {
namespace audio {
namespace format {

enum ReadWrite { READ, WRITE };

void registerFormats(AudioFormatManager* afm, ReadWrite rw);
AudioFormatManager* createAudioFormatManager(ReadWrite rw);

}  // namespace format
}  // namespace audio
}  // namespace rec

#endif  // __REC_AUDIO_REGISTERFORMATS__

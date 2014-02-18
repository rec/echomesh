// This file is derived from juce's juce_ResamplingAudioSource.h

/*
  ==============================================================================

   This file is part of the JUCE library.
   Copyright (c) 2013 - Raw Material Software Ltd.

   Permission is granted to use this software under the terms of either:
   a) the GPL v2 (or any later version)
   b) the Affero GPL v3

   Details of these licenses can be found at: www.gnu.org/licenses

   JUCE is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
   A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

   ------------------------------------------------------------------------------

   To release a closed-source product which uses JUCE, commercial licenses are
   available: visit www.juce.com for more information.

  ==============================================================================
*/

#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

//==============================================================================
/**
    A type of AudioSource that takes an input source and changes its sample rate.

    @see AudioSource
*/
class JUCE_API  ResamplingPositionableAudioSource  : public PositionableAudioSource
{
public:
    //==============================================================================
    /** Creates a ResamplingPositionableAudioSource for a given input source.

        @param inputSource              the input source to read from
        @param deleteInputWhenDeleted   if true, the input source will be deleted when
                                        this object is deleted
        @param numChannels              the number of channels to process
    */
    ResamplingPositionableAudioSource(
        PositionableAudioSource* inputSource,
        bool deleteInputWhenDeleted,
        double samplesInPerOutputSample,                                                                          int numChannels = 2);

    /** Destructor. */
    ~ResamplingPositionableAudioSource();

    /** Changes the resampling ratio.

        (This value can be changed at any time, even while the source is running).

        @param samplesInPerOutputSample     if set to 1.0, the input is passed through; higher
                                            values will speed it up; lower values will slow it
                                            down. The ratio must be greater than 0
    */
    void setResamplingRatio (double samplesInPerOutputSample);

    /** Returns the current resampling ratio.

        This is the value that was set by setResamplingRatio().
    */
    double getResamplingRatio() const noexcept                  { return ratio; }

    //==============================================================================
    void prepareToPlay (int samplesPerBlockExpected, double sampleRate) override;
    void releaseResources() override;
    void getNextAudioBlock (const AudioSourceChannelInfo&) override;

    void setLooping(bool isLooping) { input->setLooping(isLooping); }
    bool isLooping() const { return input->isLooping(); }
    void setNextReadPosition(int64 newPosition) {
        input->setNextReadPosition(static_cast<int64>(newPosition * ratio));
    }

    /** Returns the position from which the next block will be returned.

        @see setNextReadPosition
    */
    virtual int64 getNextReadPosition() const {
        return static_cast<int64>(input->getNextReadPosition() / ratio);
    }

    /** Returns the total length of the stream (in samples). */
    virtual int64 getTotalLength() const {
        return static_cast<int64>(input->getTotalLength() / ratio);
    }


private:
    //==============================================================================
    OptionalScopedPointer<PositionableAudioSource> input;
    double ratio, lastRatio;
    AudioSampleBuffer buffer;
    int bufferPos, sampsInBuffer;
    double subSampleOffset;
    double coefficients[6];
    SpinLock ratioLock;
    const int numChannels;
    HeapBlock<float*> destBuffers, srcBuffers;

    void setFilterCoefficients (double c1, double c2, double c3, double c4, double c5, double c6);
    void createLowPass (double proportionalRate);

    struct FilterState
    {
        double x1, x2, y1, y2;
    };

    HeapBlock<FilterState> filterStates;
    void resetFilters();

    void applyFilter (float* samples, int num, FilterState& fs);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (ResamplingPositionableAudioSource)
};

}  // namespace audio
}  // namespace echomesh


/*
  ==============================================================================

   This file is part of the JUCE library - "Jules' Utility Class Extensions"
   Copyright 2004-11 by Raw Material Software Ltd.

  ------------------------------------------------------------------------------

   JUCE can be redistributed and/or modified under the terms of the GNU General
   Public License (Version 2), as published by the Free Software Foundation.
   A copy of the license is included in the JUCE distribution, or can be found
   online at www.gnu.org/licenses.

   JUCE is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
   A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  ------------------------------------------------------------------------------

   To release a closed-source product which uses JUCE, commercial licenses are
   available: visit www.rawmaterialsoftware.com/juce for more information.

  ==============================================================================
*/

#ifndef __JUCE_LAGRANGEINTERPOLATOR_JUCEHEADER__
#define __JUCE_LAGRANGEINTERPOLATOR_JUCEHEADER__

//==============================================================================
/**
    Interpolator for resampling a stream of floats using 4-point lagrange interpolation.

    Note that the resampler is stateful, so when there's a break in the continuity
    of the input stream you're feeding it, you should call reset() before feeding
    it any new data. And like with any other stateful filter, if you're resampling
    multiple channels, make sure each one uses its own LagrangeInterpolator
    object.
*/
class JUCE_API  LagrangeInterpolator
{
public:
    LagrangeInterpolator();
    ~LagrangeInterpolator();

    /** Resets the state of the interpolator.
        Call this when there's a break in the continuity of the input data stream.
    */
    void reset() noexcept;

    /** Resamples a stream of samples.

        @param speedRatio       the number of input samples to use for each output sample
        @param inputSamples     the source data to read from. This must contain at
                                least (speedRatio * numOutputSamplesToProduce) samples.
        @param outputSamples    the buffer to write the results into
        @param numOutputSamplesToProduce    the number of output samples that should be created

        @returns the actual number of input samples that were used
    */
    int process (double speedRatio,
                 const float* inputSamples,
                 float* outputSamples,
                 int numOutputSamplesToProduce) noexcept;

    /** Resamples a stream of samples, adding the results to the output data
        with a gain.

        @param speedRatio       the number of input samples to use for each output sample
        @param inputSamples     the source data to read from. This must contain at
                                least (speedRatio * numOutputSamplesToProduce) samples.
        @param outputSamples    the buffer to write the results to - the result values will be added
                                to any pre-existing data in this buffer after being multiplied by
                                the gain factor
        @param numOutputSamplesToProduce    the number of output samples that should be created
        @param gain             a gain factor to multiply the resulting samples by before
                                adding them to the destination buffer

        @returns the actual number of input samples that were used
     */
    int processAdding (double speedRatio,
                       const float* inputSamples,
                       float* outputSamples,
                       int numOutputSamplesToProduce,
                       float gain) noexcept;

private:
    float lastInputSamples[5];
    double subSamplePos;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (LagrangeInterpolator)
};


#endif   // __JUCE_LAGRANGEINTERPOLATOR_JUCEHEADER__
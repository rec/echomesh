'''Analyse sound chunks

Analyse sound chunks to detect loudness and pitch.  Also includes some
utility functions for converting midi note numbers to and from
frequencies.  Designed for realtime microphone input for singing
games.

Copyright 2008, Nathan Whitehead
Released under the LGPL

'''

import numpy
import math

import analyseffi

def loudness(chunk):
    '''Calculate and return volume of input samples

    Input chunk should be a numpy array of samples for analysis, as
    returned by sound card.  Sound card should be in 16-bit mono mode.
    Return value is measured in dB, will be from 0dB (maximum
    loudness) down to -80dB (no sound).  Typical very loud sound will
    be -1dB, typical silence is -36dB.

    '''
    data = numpy.array(chunk, dtype=float) / 32768.0
    ms = math.sqrt(numpy.sum(data ** 2.0) / len(data))
    if ms < 10e-8: ms = 10e-8
    return 10.0 * math.log(ms, 10.0)


def detect_pitch(chunk, min_frequency=82.0, max_frequency=1000.0, samplerate=44100.0, sens=0.1, ratio=5.0):
    '''Return the pitch present in a chunk of sampled sound

    The chunk should be a numpy array of samples from the soundcard,
    in 16-bit mono format.  The return value will either be None if no
    pitch could be detected, or a frequency in Hz if a pitch was
    detected.  The chunk should be at least 1024 bytes long for
    accurate pitch detection of lower frequencies.

    Human vocal range is from about E2 to C6. This corresponds to
    frequencies of approx 82-1000 Hz.  Middle C is C4 at 261.6 Hz.

    Keyword arguments:
    min_frequency - minimum frequency to detect (default: 82.0)
    max_frequency - maximum frequency to detect (default: 1000.0)
    samplerate - sampling frequency of input (Hz) (default: 44100.0)
    sens - tuning parameter to avoid octave skipping
           (should be between 0.0 and 1.0, default: 0.1)
    ratio - how good detected pitch much be before being accepted,
            higher numbers are more stringent (default: 5.0)

    '''
    chunk2 = chunk.data[:]
    # Call C function to do work for us
    dp = analyseffi.detect_pitch(chunk2, min_frequency, max_frequency, samplerate, sens, ratio)
    # Now dp is either None or a number representing an offset
    if dp is not None:
        return samplerate / dp
    return None


_previous_pitch = None

def musical_detect_pitch(chunk, min_note=40.0, max_note=84.0, samplerate=44100, sens=0.1, ratio=5.0, smooth=1.0):
    '''Return the pitch present in a chunk of sampled sound

    The chunk should be a numpy array of samples from the soundcard,
    in 16-bit mono format.  The return value will either be None if no
    pitch could be detected, or a midi note number if a pitch was
    detected.  The chunk should be at least 1024 bytes long for
    accurate pitch detection of lower frequencies.  The return value
    will be a floating point number, e.g. 60.5 is half a semitone
    above middle C (60).

    Human vocal range is from about 40 (E2) to 83 (C6). This
    corresponds to frequencies of approx 82-1000 Hz.  Middle C is 60
    (C4).

    Keyword arguments:
    min_note - minimum midi note to detect (default: 40)
    max_note - maximum frequency to detect (default: 83)
    samplerate - sampling frequency of input (Hz) (default: 44100.0)
    sens - tuning parameter to avoid octave skipping
           (should be between 0.0 and 1.0, default: 0.1)
    ratio - how good detected pitch much be before being accepted,
            higher numbers are more stringent (default: 5.0)
    smooth - how much to smooth output (default: 1.0)
    
    '''
    global _previous_pitch
    freq = detect_pitch(chunk, 
                        min_frequency=pitch_from_midinum(min_note),
                        max_frequency=pitch_from_midinum(max_note),
                        samplerate=samplerate,
                        sens=sens,
                        ratio=ratio)
    if freq is not None:
        freq = midinum_from_pitch(freq)
        if smooth == 0.0: return freq
        if _previous_pitch is None:
            _previous_pitch = freq
        else:
            # a is weight of new frequency 
            #   as compared to weight of old freq (which is 1.0)
            # So if freq changes by smooth, weight old and new equally
            # Theory is that large pitch changes need to be tracked quickly
            # Small pitch changes are just noise to be smoothed out
            a = (freq - _previous_pitch) ** 2.0 / smooth
            # alpha is 0.0 to 1.0, blend from previous to new freq
            alpha = 1.0 / (a + 1.0)
            _previous_pitch = _previous_pitch * alpha + freq * (1.0 - alpha)
            return _previous_pitch
    else:
        # No pitch detected
        freq = _previous_pitch
        _previous_pitch = None
        return freq

def midinum_from_pitch(freq):
    """Return midi note number from pitch

    Midi note numbers go from 0-127, middle C is 60.  Given a frequency
    in Hz, this function computes the midi note number corresponding to
    that frequency.  The return value is a floating point number.

    """
    # formula from wikipedia on "pitch"
    if freq is None: return None
    return 69 + 12 * math.log((freq / 440.0), 2.0)

def pitch_from_midinum(m):
    """Return pitch of midi note number

    Midi note numbers go from 0-127, middle C is 60.  Given a note number
    this function computes the frequency.  The return value is a floating
    point number.

    """
    # formula from wikipedia on "pitch"
    if m is None: return None
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

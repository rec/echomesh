#ifndef __REC_BASE_REALTIME__
#define __REC_BASE_REALTIME__

#include "rec/base/SampleRate.h"

namespace rec {

struct SampleTime;

struct RealTime {
  RealTime() : time_(0) {}
  RealTime(double p) : time_(p) {}
  RealTime(float p) : time_(p) {}

  RealTime(const SampleTime&, SampleRate);

  // We need this constructor so we can construct an "empty" RealTime(0).
  // Best to avoid using.
  explicit RealTime(int time) : time_(static_cast<double>(time)) {
    //
  }


  const RealTime operator+(RealTime p) { return time_ + p; }
  const RealTime operator-(RealTime p) { return time_ - p; }

  const RealTime operator+(double p) { return time_ + p; }
  const RealTime operator-(double p) { return time_ - p; }
  const RealTime operator+(float p) { return time_ + p; }
  const RealTime operator-(float p) { return time_ - p; }

  RealTime& operator-=(RealTime t) { time_ -= t; return *this; }
  RealTime& operator+=(RealTime t) { time_ += t; return *this; }
  RealTime& operator/=(RealTime t) { time_ /= t; return *this; }
  RealTime& operator*=(RealTime t) { time_ *= t; return *this; }

  operator double() const { return time_; }

 private:
  double time_;

  // Disallow these constructors.
  RealTime(int64 time);
  RealTime(short time);

  JUCE_LEAK_DETECTOR(RealTime);
};

}  // namespace rec

#endif  // __REC_BASE_REALTIME__

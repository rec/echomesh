#ifndef __REC_BASE_SAMPLETIME__
#define __REC_BASE_SAMPLETIME__

#include "rec/base/RealTime.h"
#include "rec/base/SampleRate.h"

namespace rec {

struct SampleTime {
  SampleTime() {}

  // Conversion from integer types means "a sample count".
  SampleTime(int64 p) : position_(p) {}
  SampleTime(uint64 p) : position_(static_cast<int64>(p)) {}
  SampleTime(int p) : position_(p) {}
  SampleTime(uint p) : position_(p) {}
  SampleTime(short p) : position_(p) {}

  SampleTime(RealTime t, SampleRate rate)
      : position_(static_cast<int64>(t * rate)) {
  }

  SampleTime& operator++() { ++position_; return *this; }
  SampleTime& operator--() { --position_; return *this; }

  SampleTime operator++(int) { return position_++; }
  SampleTime operator--(int) { return position_--; }

  SampleTime& operator-=(SampleTime p) { position_ -= p; return *this; }
  SampleTime& operator+=(SampleTime p) { position_ += p; return *this; }

  const SampleTime operator+(SampleTime p) { return position_ + p; }
  const SampleTime operator-(SampleTime p) { return position_ - p; }
  const SampleTime operator+(int p) { return position_ + p; }
  const SampleTime operator+(int64 p) { return position_ + p; }
  const SampleTime operator+(uint p) { return position_ + p; }
  const SampleTime operator+(uint64 p) { return position_ + p; }
  const SampleTime operator-(int p) { return position_ - p; }
  const SampleTime operator-(int64 p) { return position_ - p; }
  const SampleTime operator-(uint p) { return position_ - p; }
  const SampleTime operator-(uint64 p) { return position_ - p; }
  const SampleTime operator-() { return -position_; }

  operator int64() const { return position_; }
  int64 get() { return position_; }

 private:
  SampleTime(RealTime time);
  SampleTime(double time);

  int64 position_;

  JUCE_LEAK_DETECTOR(SampleTime);
};

inline const SampleTime operator+(int p, SampleTime q) { return SampleTime(p) + q; }
inline const SampleTime operator+(int64 p, SampleTime q) { return SampleTime(p) + q; }
inline const SampleTime operator+(uint p, SampleTime q) { return SampleTime(p) + q; }
inline const SampleTime operator+(uint64 p, SampleTime q) { return SampleTime(p) + q; }
inline const SampleTime operator-(int p, SampleTime q) { return SampleTime(p) - q; }
inline const SampleTime operator-(int64 p, SampleTime q) { return SampleTime(p) - q; }
inline const SampleTime operator-(uint p, SampleTime q) { return SampleTime(p) - q; }
inline const SampleTime operator-(uint64 p, SampleTime q) { return SampleTime(p) - q; }


inline RealTime::RealTime(const SampleTime& t, SampleRate r) : time_(t / r) {}

}  // namespace rec

#endif  // __REC_BASE_SAMPLETIME__

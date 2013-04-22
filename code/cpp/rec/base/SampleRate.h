#ifndef __REC_BASE_SAMPLERATE__
#define __REC_BASE_SAMPLERATE__

#include "rec/base/base.h"

namespace rec {

struct SampleRate {
  SampleRate() : rate_(0.0) {}
  SampleRate(double r) : rate_(r) {}
  operator double() const { return rate_; }
  SampleRate& operator=(double r) { rate_ = r; return *this; }
  SampleRate& operator=(SampleRate r) { rate_ = r.rate_; return *this; }

 private:
  double rate_;
};

}  // namespace rec

#endif  // __REC_BASE_SAMPLERATE__

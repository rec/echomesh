#include "rec/base/RealTime.h"
#include "rec/base/SampleTime.h"

namespace rec {

RealTime::RealTime(const SampleTime& t, SampleRate r) : time_(t / r) {}

}  // namespace rec

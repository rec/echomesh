#pragma once

#include <stdio.h>

#include <iostream>
#include <string>
#include <vector>

#include <glog/logging.h>

#include "JuceLibraryCode/JuceHeader.h"
#include "echomesh/base/Disallow.h"
#include "echomesh/base/make_unique.h"
#include "rec/base/RealTime.h"
#include "rec/base/SampleTime.h"
#include "rec/base/SampleRate.h"

using std::string;
using std::vector;
using std::unique_ptr;

using rec::RealTime;
using rec::SampleTime;
using rec::SampleRate;

namespace echomesh {

const float EPSILON = 1.0 / 0x10000;

inline bool near(float scale, float value, float tolerance = EPSILON) {
  return fabsf(scale - value) < tolerance;
}

class Exception : public std::exception {
 public:
  Exception(const String& m) : message_(m) {}
  virtual ~Exception() throw() {}
  virtual const char* what() const throw() { return message_.toUTF8(); }
  virtual const String& what_str() const throw() { return message_; }

 private:
  const String message_;
};

typedef std::pair<int, int> Point;

}  // namespace echomesh


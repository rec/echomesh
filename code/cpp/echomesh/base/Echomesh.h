#ifndef __ECHOMESH__
#define __ECHOMESH__

#include <stdio.h>

#include <iostream>
#include <string>
#include <vector>

#include <glog/logging.h>

#include "JuceLibraryCode/JuceHeader.h"
#include "echomesh/base/Disallow.h"
#include "echomesh/base/Log.h"
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

// http://www.parashift.com/c++-faq/macro-for-ptr-to-memfn.html
#define CALL_MEMBER_FN(object, ptrToMember)  ((object).*(ptrToMember))

namespace rec { namespace util { namespace thread { namespace callback {
class Callback;
}}}}

namespace echomesh {

typedef rec::util::thread::callback::Callback Callback;

class Exception : public std::exception {
 public:
  Exception(const String& m) : message_(m) {}
  virtual ~Exception() throw() {}
  virtual const char* what() const throw() { return message_.toUTF8(); }
  virtual const String& what_str() const throw() { return message_; }

 private:
  const String message_;
};

typedef uint8 ColorBytes[3];
typedef std::vector<Colour> ColorList;
typedef std::vector<uint8> ByteList;

struct Point {
  Point() {}
  Point(int x_, int y_) : x(x_), y(y_) {}
  int x;
  int y;
};

}  // namespace echomesh

#endif  // __ECHOMESH__

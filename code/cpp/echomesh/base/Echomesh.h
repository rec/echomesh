#ifndef __ECHOMESH__
#define __ECHOMESH__

#include <stdio.h>

#include <iostream>
#include <string>
#include <vector>

#include "JuceLibraryCode/JuceHeader.h"
#include "echomesh/base/Disallow.h"
#include "rec/base/RealTime.h"
#include "rec/base/SampleTime.h"
#include "rec/base/SampleRate.h"

using std::string;
using std::vector;

using rec::RealTime;
using rec::SampleTime;
using rec::SampleRate;

// http://www.parashift.com/c++-faq/macro-for-ptr-to-memfn.html
#define CALL_MEMBER_FN(object, ptrToMember)  ((object).*(ptrToMember))

namespace YAML { class Node; }

namespace rec { namespace util { namespace thread { namespace callback {
class Callback; } } } }

namespace echomesh {

typedef rec::util::thread::callback::Callback Callback;
typedef YAML::Node Node;

void log(const String&);
void log2(const String&);

void close_log();

class Exception : public std::exception {
 public:
  Exception(const String& m) : message_(m) {}
  virtual ~Exception() throw() {}
  virtual const char* what() const throw() { return message_.toUTF8(); }
  virtual const String& what_str() const throw() { return message_; }

 private:
  const String message_;
};

}

#endif  // __ECHOMESH__

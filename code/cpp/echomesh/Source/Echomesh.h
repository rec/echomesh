#ifndef __ECHOMESH__
#define __ECHOMESH__

#include <stdio.h>

#include <iostream>
#include <string>
#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"

using std::string;
using std::vector;

namespace echomesh {

void log(const string&);
void close_log();

inline string str(const String& s) {
  return string(s.toUTF8());
}

inline String str(const string& s) {
  const char* p = s.c_str();
  size_t size = s.size();
  bool valid = CharPointer_UTF8::isValidString(p, size);
  if (!valid) {
    // LOG(ERROR) << "Badly encoded string |" << s << "| " << s.size();
    // LOG(ERROR) << s[0] << ", " << s[1];
  }
  return valid ? String::fromUTF8(p, size) : "(badly encoded string)";
}

inline String str(const char* s) { return str(string(s)); }

class Exception : public std::exception {
 public:
  Exception(const string& m) : message_(m) {}
  Exception(const String& m) : message_(str(m)) {}
  Exception(const char* m) : message_(m) {}
  virtual ~Exception() throw() {}
  virtual const char* what() const throw() { return message_.c_str(); }
  virtual const string& what_str() const throw() { return message_; }

 private:
  const string message_;
};

}

#endif  // __ECHOMESH__

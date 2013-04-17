#ifndef __ECHOMESH_EXCEPTION__
#define __ECHOMESH_EXCEPTION__

#include <exception>
#include "Echomesh.h"

namespace echomesh {

class Exception : public std::exception {
 public:
  explicit Exception(const string& m) : message_(m) {}
  virtual ~Exception() throw() {}
  virtual const char* what() const throw() { return message_.c_str(); }

 private:
  const string message_;
};

}  // namespace echomesh

#endif  // __ECHOMESH_EXCEPTION__

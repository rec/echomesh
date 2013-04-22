#ifndef __REC_BASE_BASE__
#define __REC_BASE_BASE__

#include <string>
#include <vector>

#include "rec/base/disallow.h"
#include "rec/base/types.h"

namespace google { namespace protobuf { class Message; }}

namespace rec {

namespace util { namespace file { class VirtualFile; }}
namespace util { namespace file { class VirtualFileList; }}

typedef unsigned int uint;

typedef google::protobuf::Message Message;
typedef std::string string;

using namespace util;

using std::pair;
using std::vector;
using util::file::VirtualFile;
using util::file::VirtualFileList;

enum Endianness { LITTLE_END, BIG_END };
enum Orientation {HORIZONTAL, VERTICAL};
enum Undoable { CANT_UNDO, CAN_UNDO };
enum Scope { FILE_SCOPE, GLOBAL_SCOPE };
enum Enable { DISABLE, ENABLE };
const int SOCKET_TIMEOUT_MS = 2000;

inline Scope scope(bool global) { return global ? GLOBAL_SCOPE : FILE_SCOPE; }

inline Orientation inverse(Orientation o) {
  return (o == HORIZONTAL) ? VERTICAL : HORIZONTAL;
}

class None {};

}  // namespace rec

#endif  // __REC_BASE_BASENOJUCE__

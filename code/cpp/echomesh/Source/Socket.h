#ifndef __REC_UTIL_CD_SOCKET__
#define __REC_UTIL_CD_SOCKET__

#include "Echomesh.h"

namespace echomesh {

void connect(StreamingSocket* sock, const String& name, int port, int timeout);
void writeStreamingSocket(StreamingSocket* sock, const String& request);
string readStreamingSocket(StreamingSocket* sock, int timeout);

}  // namespace echomesh

#endif  // __REC_UTIL_CD_SOCKET__

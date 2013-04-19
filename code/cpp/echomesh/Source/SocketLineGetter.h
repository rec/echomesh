#ifndef __ECHOMESH_SOCKET_LINE_GETTER__
#define __ECHOMESH_SOCKET_LINE_GETTER__

#include "LineGetter.h"

namespace echomesh {

class LineQueue;

class SocketLineGetter : public LineGetter {
 public:
  SocketLineGetter(const String& server, int port, int timeout, int bufferSize);
  virtual ~SocketLineGetter();

  virtual string getLine();
  virtual bool eof() const { return !socket_.isConnected(); }

 private:
  string readSocket();

  StreamingSocket socket_;
  const int timeout_;
  vector<char> buffer_;

  ScopedPointer<LineQueue> lineQueue_;

  DISALLOW_COPY_AND_ASSIGN(SocketLineGetter);
};

}  // namespace echomesh

#endif __ECHOMESH_SOCKET_LINE_GETTER__

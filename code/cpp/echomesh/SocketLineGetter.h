#ifndef __ECHOMESH_SOCKET_LINE_GETTER__
#define __ECHOMESH_SOCKET_LINE_GETTER__

#include "echomesh/LineGetter.h"

namespace echomesh {

class LineQueue;

struct SocketDescription {
  String server;
  int port;
  int timeout;
  int bufferSize;
  int tries;
  int retryTimeout;
};

class SocketLineGetter : public LineGetter {
 public:
  SocketLineGetter(const SocketDescription&);
  virtual ~SocketLineGetter();

  virtual string getLine();
  virtual bool eof() const { return eof_; }

 private:
  string readSocket();
  void fail(const String&);

  StreamingSocket socket_;
  vector<char> buffer_;
  const SocketDescription desc_;
  bool connected_;
  bool eof_;

  ScopedPointer<LineQueue> lineQueue_;

  DISALLOW_COPY_AND_ASSIGN(SocketLineGetter);
};

}  // namespace echomesh

#endif  // __ECHOMESH_SOCKET_LINE_GETTER__

#ifndef __ECHOMESH_SOCKET_LINE_GETTER__
#define __ECHOMESH_SOCKET_LINE_GETTER__

#include "LineGetter.h"

namespace echomesh {

class LineQueue;

struct SocketDescription {
  String server;
  int port;
  int timeout;
  int bufferSize;
  int retries;
  int retryTimeout;
};

class SocketLineGetter : public LineGetter {
 public:
  SocketLineGetter(const SocketDescription&);
  virtual ~SocketLineGetter();

  virtual string getLine();
  virtual bool eof() const { return not (connected_ and socket_.isConnected()); }

 private:
  string readSocket();

  StreamingSocket socket_;
  vector<char> buffer_;
  const SocketDescription desc_;
  bool connected_;

  ScopedPointer<LineQueue> lineQueue_;

  DISALLOW_COPY_AND_ASSIGN(SocketLineGetter);
};

}  // namespace echomesh

#endif __ECHOMESH_SOCKET_LINE_GETTER__

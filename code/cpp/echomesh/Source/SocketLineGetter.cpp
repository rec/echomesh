#include "SocketLineGetter.h"
#include "LineQueue.h"

namespace echomesh {

SocketLineGetter::SocketLineGetter(const String& server, int port, int timeout,
                                   int bufferSize)
    : timeout_(timeout),
      buffer_(bufferSize),
      lineQueue_(new LineQueue) {
  if (int error = !socket_.connect(server, port, timeout)) {
    throw Exception("Error " + String(error) + " connecting to " +
                    server + ":" + String(port));
  }
}

SocketLineGetter::~SocketLineGetter() {}

string SocketLineGetter::getLine() {
  while (!lineQueue_->empty())
    lineQueue_->push(readSocket());
  return lineQueue_->pop();
}

string SocketLineGetter::readSocket() {
  if (!socket_.isConnected())
    throw Exception("StreamingSocket: Not connected.");

  int isReady = socket_.waitUntilReady(true, timeout_);
  if (isReady < 0)
    throw Exception("StreamingSocket wait error");

  int read = 0;
  if (isReady > 0) {
    read = socket_.read(&buffer_.front(), buffer_.size(), false);
    if (read < 0)
      throw Exception("StreamingSocket read error " + String(read));
  }
  return string(&buffer_.front(), read);
}

}  // namespace echomesh

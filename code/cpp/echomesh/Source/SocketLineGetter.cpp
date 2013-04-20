#include "SocketLineGetter.h"
#include "LineQueue.h"

namespace echomesh {

SocketLineGetter::SocketLineGetter(const SocketDescription& desc)
    : desc_(desc), connected_(false) {
}

SocketLineGetter::~SocketLineGetter() {}

string SocketLineGetter::getLine() {
  while (lineQueue_->empty())
    lineQueue_->push(readSocket());
  return lineQueue_->pop();
}

string SocketLineGetter::readSocket() {
  for (int connectionAttempts = 0; !connected_; ++connectionAttempts) {
    if (connectionAttempts and connectionAttempts > desc_.retries)
      throw Exception("Failed to connect to socket.");
    connected_ = socket_.connect(desc_.server, desc_.port, desc_.retryTimeout);
  }

  while (true) {
    if (!socket_.isConnected())
      throw Exception("StreamingSocket: Socket disconnected.");

    int isReady = socket_.waitUntilReady(true, desc_.timeout);
    if (!isReady)
      continue;

    if (isReady < 0)
      throw Exception("StreamingSocket wait error");

    int read = socket_.read(&buffer_.front(), buffer_.size(), false);
    if (read < 0)
      throw Exception("StreamingSocket read error " + String(read));
    if (read)
      return string(&buffer_.front(), read);
  }
}

}  // namespace echomesh

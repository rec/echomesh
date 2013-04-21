#include "SocketLineGetter.h"
#include "LineQueue.h"

namespace echomesh {

SocketLineGetter::SocketLineGetter(const SocketDescription& desc)
    : buffer_(desc.bufferSize), desc_(desc), connected_(false), eof_(false),
      lineQueue_(new LineQueue) {
}

SocketLineGetter::~SocketLineGetter() {}

string SocketLineGetter::getLine() {
  if (lineQueue_->empty())
    lineQueue_->push(readSocket());
  if (lineQueue_->empty())
    log("OOOOOOOPS");
  return lineQueue_->pop();
}

string SocketLineGetter::readSocket() {
  for (int connectionAttempts = 0; !connected_; ++connectionAttempts) {
    if (desc_.tries > 0 and connectionAttempts > desc_.tries) {
      log("Failed to connect");
      throw Exception("Failed to connect to socket.");
    }
    connected_ = socket_.connect(desc_.server, desc_.port, desc_.retryTimeout);
    if (connected_)
      log("!connected!");
  }

  while (true) {
    if (!socket_.isConnected()) {
      eof_ = true;
      log("disconnected");
      throw Exception("StreamingSocket: Socket disconnected.");
    }

    int isReady = socket_.waitUntilReady(true, desc_.timeout);
    if (!isReady)
      continue;

    if (isReady < 0)
      throw Exception("StreamingSocket wait error");

    int read = socket_.read(&buffer_.front(), buffer_.size(), false);
    if (read < 0)
      throw Exception("StreamingSocket read error " + String(read));
    if (read) {
      log("got data \"" + string(&buffer_.front(), read) + "\"");
      return string(&buffer_.front(), read);
    } else {
      log("read 0");
    }
  }
}

}  // namespace echomesh

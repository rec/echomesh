#include "echomesh/SocketLineGetter.h"

#include "echomesh/LineQueue.h"

namespace echomesh {

SocketLineGetter::SocketLineGetter(const SocketDescription& desc)
    : buffer_(desc.bufferSize), desc_(desc), connected_(false), eof_(false),
      lineQueue_(new LineQueue) {
}

SocketLineGetter::~SocketLineGetter() {}

string SocketLineGetter::getLine() {
  if (lineQueue_->empty())
    lineQueue_->push(readSocket());
  return lineQueue_->pop();
}

void SocketLineGetter::check(bool condition, const String& msg) {
  if (!condition) {
    eof_ = true;
    throw Exception(msg);
  }
}

string SocketLineGetter::readSocket() {
  for (int attempts = 0; !connected_; ++attempts) {
    check(not desc_.tries or attempts <= desc_.tries, "Failed to connect");
    connected_ = socket_.connect(desc_.server, desc_.port, desc_.retryTimeout);
  }

  while (true) {
    check(socket_.isConnected(), "StreamingSocket: Socket disconnected.");

    int isReady = socket_.waitUntilReady(true, desc_.timeout);
    if (not isReady)
      continue;

    check(isReady >= 0, "StreamingSocket wait error");
    check(socket_.isConnected(), "Socket was ready, then disconnected.");

    int read = socket_.read(&buffer_.front(), buffer_.size(), false);
    check(read, "Socket was ready, but got zero data.");
    check(read > 0, "StreamingSocket read error");
    return string(&buffer_.front(), read);
  }
}

}  // namespace echomesh

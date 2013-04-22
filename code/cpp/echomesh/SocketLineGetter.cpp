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

void SocketLineGetter::fail(const String& msg) {
  eof_ = true;
  throw Exception(msg);
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
    if (not socket_.isConnected())
      fail("StreamingSocket: Socket disconnected.");

    int isReady = socket_.waitUntilReady(true, desc_.timeout);
    if (not isReady)
      continue;

    if (isReady < 0)
      fail("StreamingSocket wait error");

    if (not socket_.isConnected())
      fail("Socket was ready, then disconnected.");

    int read = socket_.read(&buffer_.front(), buffer_.size(), false);
    if (read < 0)
      fail("StreamingSocket read error " + String(read));

    if (not read)
      fail("Socket was ready, but got zero data.");

    return string(&buffer_.front(), read);
  }
}

}  // namespace echomesh

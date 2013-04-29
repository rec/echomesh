#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/network/LineQueue.h"

namespace echomesh {

static SocketLineGetter* INSTANCE = NULL;

SocketLineGetter::SocketLineGetter(const SocketDescription& desc)
    : buffer_(desc.bufferSize), desc_(desc), connected_(false), eof_(false),
      lineQueue_(new LineQueue) {
  INSTANCE = this;
}

SocketLineGetter::~SocketLineGetter() {
  INSTANCE = NULL;
}

SocketLineGetter* SocketLineGetter::instance() {
  return INSTANCE;
}

string SocketLineGetter::getLine() {
  while (lineQueue_->empty())
    lineQueue_->push(readSocket());
  return lineQueue_->pop();
}

void SocketLineGetter::check(bool condition, const String& msg) {
  if (!condition) {
    eof_ = true;
    throw Exception(msg);
  }
}

static const char YAML_SEPARATOR[] = "\n---\n";

void SocketLineGetter::writeSocket(const char* data, int size) {
  string s(data, size);
  s += YAML_SEPARATOR;

  tryToConnect();
  if (socket_.write(s.data(), s.size()) < 0)
    log("ERROR writing data.");
}

void SocketLineGetter::tryToConnect() {
  for (int attempts = 0; !connected_; ++attempts) {
    check(not desc_.tries or attempts <= desc_.tries, "Failed to connect");
    connected_ = socket_.connect(desc_.server, desc_.port, desc_.retryTimeout);
  }
}

string SocketLineGetter::readSocket() {
  tryToConnect();
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

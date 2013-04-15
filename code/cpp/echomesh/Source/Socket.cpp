#include "rec/util/cd/Socket.h"
#include "rec/util/Exception.h"

using namespace juce;

namespace echomesh {

static const int BUFFER_SIZE = 4096;

void writeSocket(Socket* sock, const String& s) {
  // There's an extra copy here that could be removed.
  int w = sock->write(str(s).c_str(), s.length());
  if (w != s.length()) {
    throw Exception(string("Wrote ") + String(w) + " of " + String(s.length()) + " chars.");
  }
}

string readSocket(Socket* sock, int timeout) {
  char buffer[BUFFER_SIZE];

  int error = sock->waitUntilReady(true, timeout);
  if (error <= 0)
    throw Exception("Socket wait error " + error);

  int read = sock->read(buffer, BUFFER_SIZE, false);
  if (read <= 0)
    throw Exception("Socket read error " + read);

  return string(buffer, read);
}

void connect(Socket* s, const String& server, int port, int timeout) {
  if (!s->connect(server, port, timeout)) {
    throw Exception(str("Couldn't open socket to " +
                    server + ":" + String(port)));
  }
}

}  // namespace echomesh

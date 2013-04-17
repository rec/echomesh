#include "Socket.h"
#include "Exception.h"

using namespace juce;
using namespace std;

namespace echomesh {

static const int BUFFER_SIZE = 4096;

void writeSocket(StreamingSocket* sock, const String& s) {
  // There's an extra copy here that could be removed.
  int w = sock->write(str(s).c_str(), s.length());
  if (w != s.length()) {
    throw Exception(string("Wrote ") + str(String(w)) + " of " +
                    str(String(s.length())) + " chars.");
  }
}

string readSocket(StreamingSocket* sock, int timeout) {
  char buffer[BUFFER_SIZE];

  int error = sock->waitUntilReady(true, timeout);
  if (error <= 0)
    throw Exception("StreamingSocket wait error " + error);

  int read = sock->read(buffer, BUFFER_SIZE, false);
  if (read <= 0)
    throw Exception("StreamingSocket read error " + read);

  return string(buffer, read);
}

void connect(StreamingSocket* s, const String& server, int port, int timeout) {
  if (!s->connect(server, port, timeout)) {
    throw Exception(str("Couldn't open socket to " +
                    server + ":" + String(port)));
  }
}

}  // namespace echomesh

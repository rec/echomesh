#include "echomesh/network/LineGetter.h"
#include "echomesh/network/SocketLineGetter.h"

namespace echomesh {

// host_name port timeout buffer_size

LineGetter* makeLineGetter(const String& command) {
  StringArray parts;
  // parts.addTokens(command, false);
  SocketDescription desc;
  // desc.server = (parts.size() > 0) ? parts[0] : String("localhost");
  desc.server = (parts.size() > 0) ? parts[0] : String("127.0.0.1");
  desc.port = (parts.size() > 1) ? parts[1].getIntValue() : 1239;
  desc.timeout = 1000 * ((parts.size() > 2) ? parts[2].getFloatValue() : 1.0);
  desc.bufferSize = (parts.size() > 3) ? parts[3].getIntValue() : 4096;
  desc.debug = (parts.size() <= 4) or parts[4].toLowerCase() == "true";
  desc.tries = 0;
  desc.retryTimeout = 1000;

  if (not desc.port) {
    log("No port in LineGetter");
    throw Exception("No port in LineGetter");
  }

  return new SocketLineGetter(desc);
}

}  // namespace echomesh

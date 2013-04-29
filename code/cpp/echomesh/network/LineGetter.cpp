#include "echomesh/network/LineGetter.h"
#include "echomesh/network/SocketLineGetter.h"

namespace echomesh {

namespace {

String DEFAULT_GETTER("socket");

class CinLineGetter : public LineGetter {
 public:
  virtual string getLine() {
    string s;
    std::getline(std::cin, s);
    return s;
  }

  virtual bool eof() const { return std::cin.eof(); }
};

class FileLineGetter : public LineGetter {
 public:
  explicit FileLineGetter(const String& f)
      : stream_(new std::ifstream(f.toUTF8(), std::ifstream::in)) {
  }

  virtual string getLine() {
    string s;
    std::getline(*stream_, s);
    return s;
  }

  virtual bool eof() const { return stream_->eof(); }

 private:
  ScopedPointer<std::ifstream> stream_;

  DISALLOW_COPY_AND_ASSIGN(FileLineGetter);
};

}  // namespace

// Three possible command lines:
//   file <filename>
//   socket host_name port timeout buffer_size
//   terminal

LineGetter* makeLineGetter(const String& command) {
  StringArray parts;
  parts.addTokens(command, false);
  String cmd = parts.size() ? parts[0] : DEFAULT_GETTER;

  if (cmd == "file")
    return new FileLineGetter(parts[1].trim());

  if (cmd == "socket") {
    SocketDescription desc;
    desc.server = (parts.size() > 1) ? parts[1] : String("localhost");
    desc.port = (parts.size() > 2) ? parts[2].getIntValue() : 1239;
    desc.timeout = 1000 * ((parts.size() > 3) ? parts[3].getFloatValue() : 1.0);
    desc.bufferSize = (parts.size() > 4) ? parts[4].getIntValue() : 4096;
    desc.tries = 0;
    desc.retryTimeout = 1000;
    return new SocketLineGetter(desc);
  }

  if (cmd == "terminal")
    return new CinLineGetter;

  throw Exception("Didn't understand command line \"" + command + "\", " + cmd);
}

}  // namespace echomesh

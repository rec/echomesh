#include "LineGetter.h"
#include "SocketLineGetter.h"

namespace echomesh {

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
  explicit FileLineGetter(const string& f)
      : stream_(new std::ifstream(f.c_str(), std::ifstream::in)) {
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


//
// Command line:
//
// 1.  file <filename>
// 2.  stdin
// 3.  socket host_name port timeout buffer_size

LineGetter* makeLineGetter(const String& command) {
  log("makeLineGetter " + str(command));
  StringArray parts;
  parts.addTokens(command, false);

  if (command.startsWith("file")) {
    log("FileLineGetter");
    return new FileLineGetter(str(parts[1].trim()));
  }

  if (command.startsWith("socket")) {
    log("SocketLineGetter");
    SocketDescription desc;
    desc.server = parts[1];
    desc.port = parts[2].getIntValue();
    desc.timeout = 1000 * parts[3].getFloatValue();
    desc.bufferSize = parts[4].getIntValue();
    desc.retries = 20;
    desc.retryTimeout = 100;
    return new SocketLineGetter(desc);
  }

  return new CinLineGetter;
}

}  // namespace echomesh

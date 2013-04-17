#include "LineGetter.h"

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

class SocketLineGetter : public LineGetter {
 public:
  SocketLineGetter(const String& server, int port, int timeout, int bufferSize);

  virtual string getLine();
  virtual bool eof() const { return error_ || socket_.isConnected(); }

 private:
  string readSocket();

  StreamingSocket socket_;
  const int timeout_;
  bool error_;
  vector<char> buffer_;
  std::queue<string> lines_;
  std::string carry_;

  DISALLOW_COPY_AND_ASSIGN(SocketLineGetter);
};

SocketLineGetter::SocketLineGetter(const String& server, int port, int timeout,
                                   int bufferSize)
    : timeout_(timeout),
      buffer_(bufferSize) {
  error_ = !socket_.connect(server, port, timeout);
}

string SocketLineGetter::getLine() {
  log("SocketLineGetter::getLine");
  while (lines_.empty()) {
    string read = readSocket();
    if (read.size()) {
      int pos = read.find('\n') + 1;
      if (pos) {
        carry_ += read;
      } else {
        lines_.push(carry_ + read.substr(0, pos));
        carry_ = "";
        while (true) {
          int old_pos = pos;
          pos = read.find('\n', pos) + 1;
          if (pos)
            lines_.push(read.substr(old_pos, pos));
          else
            break;
        }
      }
    }
  }

  string res = lines_.front();
  lines_.pop();
  return res;
}

string SocketLineGetter::readSocket() {
  string result;
  int error = socket_.waitUntilReady(true, timeout_);
  if (error <= 0) {
    // throw Exception("StreamingSocket wait error " + error);
    log("socket waiting error");
    error_ = true;
  } else {
    int read = socket_.read(&buffer_.front(), buffer_.size(), false);
    if (read >= 0)
      result = string(&buffer_.front(), read);
    else
      error_ = true;
    if (error_)
      log("SocketLineGetter:readSocket: " + result);
    else
      log("SocketLineGetter:readSocket ERROR");

    // throw Exception("StreamingSocket read error " + read);
  }

  return result;
}


//
// Command line:
//
// 1.  file <filename>
// 2.  stdin
// 3.  socket host_name port timeout buffer_size

LineGetter* makeLineGetter(const String& command) {
  StringArray parts;
  parts.addTokens(command, false);

  if (command.startsWith("file"))
    return new FileLineGetter(str(parts[1].trim()));

  if (command.startsWith("socket")) {
    const String& hostName = parts[1];
    int port = parts[2].getIntValue();
    int timeout = 1000 * parts[3].getFloatValue();
    int bufferSize = parts[4].getIntValue();
    return new SocketLineGetter(hostName, port, timeout, bufferSize);
  }

  return new CinLineGetter;
}

}  // namespace echomesh

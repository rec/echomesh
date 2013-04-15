#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "ReadThread.h"
#include "LightComponent.h"

namespace echomesh {

using namespace std;

static const char READ_FILE[] = "/development/echomesh/incoming.data";

ReadThread::ReadThread(const String& commandLine)
    : Thread("ReadThread"),
      stream_(*READ_FILE ? new ifstream(READ_FILE, ifstream::in) : &cin),
      commandLine_(commandLine) {
}

ReadThread::~ReadThread() {
  if (*READ_FILE)
    delete stream_;
}

void ReadThread::run() {
  string s;
  String st;
  while (!stream_->eof()) {
    s.clear();
    log("in...");
    getline(*stream_, s);
    // cout << ".\n";
    log("in: '" + s + "'");
    if (s.find("---")) {
      accum_.add(s.c_str());
    } else {
      String result = accum_.joinIntoString("\n");
      accum_.clear();
      handleMessage(string(result.toUTF8()));
    }
  }
  log("eof!");
  quit();
}

namespace {

OutputStream* STREAM = NULL;
CriticalSection lock_;
const char FILENAME[] = "/tmp/echomesh.log";

}  // namespace

void log(const string& msg) {
  ScopedLock l(lock_);
  if (!STREAM) {
    File f(FILENAME);
    f.deleteFile();
    STREAM = new FileOutputStream(f);
  }
  STREAM->write(msg.data(), msg.size());
  STREAM->write("\n", 1);
  STREAM->flush();
}

void close_log() {
  delete STREAM;
}

}  // namespace echomesh

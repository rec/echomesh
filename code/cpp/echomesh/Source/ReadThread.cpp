#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "ReadThread.h"
#include "LightComponent.h"
#include "LineGetter.h"

namespace echomesh {

using namespace std;

static const char READ_FILE[] = "/development/echomesh/incoming.data";

ReadThread::ReadThread(const String& commandLine)
    : Thread("ReadThread"),
      lineGetter_(makeLineGetter(commandLine)) {
}

ReadThread::~ReadThread() {}

void ReadThread::run() {
  string s;
  while (!lineGetter_->eof()) {
    log("in...");
    s = lineGetter_->getLine();
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

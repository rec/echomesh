#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

using namespace std;

namespace {

CriticalSection lock_;

static const bool LOG_TO_STDOUT = true;

const char FILENAME[] = "/tmp/echomesh.log";
OutputStream* STREAM = NULL;

const char FILENAME2[] = "/tmp/echomesh.socket.log";
OutputStream* STREAM2 = NULL;

}  // namespace

void log(const String& msg) {
  if (LOG_TO_STDOUT) {
    std::cout << msg << "\n";
    std::cout.flush();
    return;
  }
  if (!*FILENAME)
    return;
  ScopedLock l(lock_);
  if (!STREAM) {
    File f(FILENAME);
    f.deleteFile();
    STREAM = new FileOutputStream(f);
  }
  STREAM->writeString(msg);
  STREAM->write("\n", 1);
  STREAM->flush();
}

void log2(const String& msg) {
  if (!*FILENAME2)
    return;
  ScopedLock l(lock_);
  if (!STREAM2) {
    File f(FILENAME2);
    f.deleteFile();
    STREAM2 = new FileOutputStream(f);
  }
  STREAM2->writeString(msg);
  // STREAM2->write("\n", 1);
  STREAM2->flush();
}

void close_log() {
  delete STREAM;
  STREAM = NULL;

  delete STREAM2;
  STREAM2 = NULL;
}

}  // namespace echomesh

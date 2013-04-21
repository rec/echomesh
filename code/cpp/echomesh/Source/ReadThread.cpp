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
    try {
      s = lineGetter_->getLine();
    } catch (Exception e) {
      log("ERROR: " + e.what_str());
      break;
    }
    log("received: " + s);
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

}  // namespace echomesh

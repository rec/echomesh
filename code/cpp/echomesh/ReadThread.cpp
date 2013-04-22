#include <stdio.h>

#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/LightComponent.h"
#include "echomesh/LineGetter.h"
#include "echomesh/ReadThread.h"

namespace echomesh {

using namespace std;

ReadThread::ReadThread(const String& commandLine)
    : Thread("ReadThread"),
      lineGetter_(makeLineGetter(commandLine)) {
}

ReadThread::~ReadThread() {}

void ReadThread::run() {
  string s;
  while (not (threadShouldExit() or lineGetter_->eof())) {
    try {
      s = lineGetter_->getLine();
    } catch (Exception e) {
      log("ERROR: " + e.what_str());
      break;
    }
    if (s.find("---")) {
      accum_.add(s.c_str());
    } else {
      String result = accum_.joinIntoString("\n");
      accum_.clear();
      handleMessage(string(result.toUTF8()));
    }
  }
  quit();
}

void ReadThread::kill() {
  signalThreadShouldExit();
  waitForThreadToExit(1000);
  stopThread(1000);
}

}  // namespace echomesh

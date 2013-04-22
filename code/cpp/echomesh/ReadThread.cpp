#include <stdio.h>

#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/LightComponent.h"
#include "echomesh/LineGetter.h"
#include "echomesh/ReadThread.h"

#include "rec/util/thread/Callback.h"

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

void ReadThread::handleMessage(const string& str) {
  istringstream s(str);
  try {
    YAML::Parser parser(s);
    if (parser.GetNextDocument(node_)) {
      node_["type"] >> type_;
      MessageMap::iterator i = messageMap_.find(type_);
      if (i == messageMap_.end()) {
        log("Didn't find message type " + type_);        parseNode();
      } else {
        (*i->second)();
      }

    } else {
      log("Didn't find a document in this input!");
    }
  } catch (YAML::Exception& e) {
    log(string("ERROR: ") + e.what() + ("in:\n" + str));
  }
}

}  // namespace echomesh

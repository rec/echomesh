#include <stdio.h>

#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/network/LineGetter.h"
#include "echomesh/network/ReadThread.h"

#include "rec/util/thread/Callback.h"
#include "rec/util/STL.h"

namespace echomesh {

using namespace std;

ReadThread::ReadThread(const String& commandLine)
    : Thread("ReadThread"),
      lineGetter_(makeLineGetter(commandLine)) {
}

ReadThread::~ReadThread() {
  rec::stl::deleteMapPointers(&messageMap_);
}

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
      accum_.add(String(s.data(), s.size()));
    } else {
      String result = accum_.joinIntoString("\n");
      if (result.indexOfChar('\0') + 1)
        log("Contains \\0:\n" + result);
      accum_.clear();
      handleMessage(result.toStdString());
    }
  }
  quit();
}

void ReadThread::handleMessage(const string& str) {
  istringstream s(str);
  try {
    YAML::Parser parser(s);
    if (parser.GetNextDocument(node_)) {
      node_["type"] >> type_;
      MessageMap::iterator i = messageMap_.find(type_);
      if (i == messageMap_.end()) {
        log("Didn't find message type " + type_);
        parseNode();
      } else {
        (*i->second)();
      }

    } else {
      log("Didn't find a document in this input!");
    }
  } catch (YAML::Exception& e) {
    // log(string("ERROR: ") + e.what() + (" in:\n" + str));
    log(string("ERROR: ") + e.what() + (" in:\n" + str.substr(0, 20)));
  }
}

}  // namespace echomesh

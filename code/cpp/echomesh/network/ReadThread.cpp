#include <stdio.h>

#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/base/Quit.h"
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
  string s, str;
  while (not (threadShouldExit() or lineGetter_->eof())) {
    try {
      s = lineGetter_->getLine();
      if (s.find("---")) {  // If we don't find a separator.
        accum_.add(String(s.data(), s.size()));
        continue;
      }

      parse(accum_.joinIntoString("\n").toStdString());
      accum_.clear();
    } catch (YAML::Exception& e) {
      log(string("Yaml parsing error: ") + e.what() + (" in:\n" + str));
    } catch (Exception e) {
      log("ERROR: " + e.what_str());
      break;
    }
  }
  ::echomesh::quit();
}

void ReadThread::parse(const string& str) {
  ScopedLock l(lock_);
  istringstream s(str);
  YAML::Parser parser(s);
  parser.GetNextDocument(node_);
  node_["type"] >> type_;
  MessageMap::iterator i = messageMap_.find(type_);
  if (i == messageMap_.end())
    log("Didn't find message type " + type_);
  else
    (*i->second)();
}

}  // namespace echomesh

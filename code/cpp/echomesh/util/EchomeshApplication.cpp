#include "echomesh/util/EchomeshApplication.h"

namespace echomesh {

namespace {

class KeyboardThread : public Thread {
 public:
  KeyboardThread(StringCaller caller, void* callback)
      : Thread("keyboard"), caller_(caller), callback_(callback) {
  }

  virtual void run() {
    string data;
    std::cin >> data;
    caller_(callback_, data);
  }

 private:
  StringCaller const caller_;
  void* const callback_;

  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(KeyboardThread);
};

unique_ptr<KeyboardThread> KEYBOARD_THREAD;

VoidCaller CALLBACK;
void* USER_DATA;

class ApplicationBase : public juce::JUCEApplicationBase {
 public:
  virtual const String getApplicationName() { return "echomesh"; }
  virtual const String getApplicationVersion() { return "0.0"; }
  virtual bool moreThanOneInstanceAllowed() { return false; }
  virtual void initialise(const String&) {
    if (CALLBACK and USER_DATA)
      CALLBACK(USER_DATA);
  }
  virtual void shutdown() {
    KEYBOARD_THREAD->stopThread(1000);
  }
  virtual void anotherInstanceStarted(const String&) {}
  virtual void systemRequestedQuit() {
    stopApplication();
  }
  virtual void suspended() {}
  virtual void resumed() {}
  virtual void unhandledException(
      const std::exception*, const String& sourceFilename, int lineNumber) {
  }
};

const char* ARGV[] = {"echomesh"};

juce::JUCEApplicationBase* juce_CreateApplication() {
  return new ApplicationBase();
}

}  // namespace

void startApplication(VoidCaller cb, void* userData) {
  CALLBACK = cb;
  USER_DATA = userData;
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
  juce::JUCEApplicationBase::main(1, ARGV);
}

void stopApplication() {
  DLOG(INFO) << "Quitting juce";
  juce::JUCEApplicationBase::quit();
}

void writeConsole(const string& data) {
  std::cout << data;
}

void flushConsole() {
  std::cout.flush();
}

void readConsole(StringCaller caller, void* callback) {
  KEYBOARD_THREAD = make_unique<KeyboardThread>(caller, callback);
  KEYBOARD_THREAD->startThread();
}

}  // namespace echomesh

#include "echomesh/LightComponent.h"
#include "echomesh/LightReader.h"

class Echomesh  : public JUCEApplication {
 public:
  Echomesh() {}

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return true; }

  void initialise (const String& commandLine) {
    mainWindow_ = new MainWindow();

    // TODO: we don't store this because it causes an error when it gets
    // deleted at shutdown - so rather have a memory leak!
    readThread_ = new echomesh::LightReader(mainWindow_->comp_, commandLine);
    readThread_->startThread();
  }

  void shutdown() {
    echomesh::log("shutting down");
    readThread_->signalThreadShouldExit();
    readThread_->waitForThreadToExit(1000);
    readThread_->stopThread(1000);
    mainWindow_ = nullptr;
  }

  void anotherInstanceStarted (const String& commandLine) {}

  class MainWindow : public DocumentWindow {
   public:
    MainWindow()  : DocumentWindow("echomesh lighting simulator",
                                   Colours::lightgrey,
                                   DocumentWindow::allButtons) {
      comp_ = new echomesh::LightComponent(this);
      setContentOwned(comp_, true);

      centreWithSize(getWidth(), getHeight());
      setVisible(true);
      setUsingNativeTitleBar(true);
    }

    void closeButtonPressed() {
      JUCEApplication::getInstance()->systemRequestedQuit();
    }

    echomesh::LightComponent* comp_;

   private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainWindow)
  };

 private:
  ScopedPointer<MainWindow> mainWindow_;
  ScopedPointer<echomesh::LightReader> readThread_;
};

START_JUCE_APPLICATION(Echomesh)

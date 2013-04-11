#include "../JuceLibraryCode/JuceHeader.h"
#include "LightComponent.h"
#include "ReadThread.h"

class Echomesh  : public JUCEApplication {
 public:
  Echomesh() {}

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return true; }

  void initialise (const String& commandLine) {
    mainWindow = new MainWindow();

    // TODO: we don't store this because it causes an error when it gets
    // deleted at shutdown - so rather have a memory leak!
    (new echomesh::ReadThread(mainWindow->comp_))->startThread();
  }

  void shutdown() {
    mainWindow = nullptr;
  }

  void systemRequestedQuit() {}
  void anotherInstanceStarted (const String& commandLine) {}

  class MainWindow : public DocumentWindow {
   public:
    MainWindow()  : DocumentWindow("MainWindow",
                                   Colours::lightgrey,
                                   DocumentWindow::allButtons) {
      comp_ = new echomesh::LightComponent;
      setContentOwned(comp_, true);

      centreWithSize(getWidth(), getHeight());
      setVisible(true);
    }

    void closeButtonPressed() {
      JUCEApplication::getInstance()->systemRequestedQuit();
    }

    echomesh::LightComponent* comp_;

   private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainWindow)
  };

 private:
  ScopedPointer<MainWindow> mainWindow;
  ScopedPointer<echomesh::ReadThread> readThread_;
};


START_JUCE_APPLICATION(Echomesh)

#include "echomesh/component/LightingWindow.h"
#include "echomesh/util/Quit.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {

LightingWindow::LightingWindow()
  : DocumentWindow("echomesh lighting simulator",
                   Colours::lightgrey,
                   DocumentWindow::allButtons),
    instrumentGrid_(new echomesh::InstrumentGrid),
    runningInTest_(false) {
  setContentOwned(instrumentGrid_, true);
  centreWithSize(getWidth(), getHeight());
  setUsingNativeTitleBar(true);
}

LightingWindow::~LightingWindow() {}

void LightingWindow::closeButtonPressed() {
  if (runningInTest_) {
    quit();

  } else {
#if 0
    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "hide"
#endif
  }
}

void LightingWindow::moved() {
#if 0
  if (false) {
    if (SocketLineGetter* getter = SocketLineGetter::instance()) {
      YAML::Emitter out;

      out << YAML::BeginMap
          << YAML::Key << "type"
          << YAML::Value << "move"
          << YAML::Key << "top_left"
          << YAML::Value << YAML::BeginSeq
          << getX() << getY() - getTitleBarHeight()
          << YAML::EndSeq
          << YAML::EndMap;

      getter->writeSocket(out.c_str(), out.size());
    }
  }
#endif
}

void LightingWindow::saveSnapshotToFile(const string& name) {
  File file(name);
  if (ImageFileFormat* format =
      ImageFileFormat::findImageFormatForFileExtension(file)) {
    Image image = createComponentSnapshot(getLocalBounds());
    FileOutputStream stream(file);
    if (not format->writeImageToStream(image, stream))
      DLOG(FATAL) << "Unable to write to filename " << name;
  } else {
    DLOG(FATAL) << "Don't understand filename " << name;
  }
}


LightingWindow* makeLightingWindow() {
  MessageManagerLock l;
  unique_ptr<LightingWindow> window = make_unique<LightingWindow>();
  window->toFront(true);
  window->setVisible(true);
  window->grid()->setLightCount(256);
  return window.release();
}

static void deleteWindow(LightingWindow* window) {
  delete window;
}

void deleteLightingWindow(LightingWindow* window) {
  runOnMessageThread(deleteWindow, window);
}

}  // namespace echomesh

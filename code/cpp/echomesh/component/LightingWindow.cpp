#include "echomesh/component/LightingWindow.h"
#include "echomesh/util/Quit.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {

LightingWindow::LightingWindow()
  : DocumentWindow("echomesh lighting simulator",
                   Colours::lightgrey,
                   DocumentWindow::allButtons),
    instrumentGrid_(new echomesh::InstrumentGrid) {
  setContentOwned(instrumentGrid_, true);
  centreWithSize(getWidth(), getHeight());
  setUsingNativeTitleBar(true);
}

LightingWindow::~LightingWindow() {}

void LightingWindow::saveSnapshotToFile(const string& name) {
  File file(name);
  if (auto format = ImageFileFormat::findImageFormatForFileExtension(file)) {
    auto image = createComponentSnapshot(getLocalBounds());
    FileOutputStream stream(file);
    if (not format->writeImageToStream(image, stream))
      LOG(DFATAL) << "Unable to write to filename " << name;
  } else {
    LOG(DFATAL) << "Don't understand filename " << name;
  }
}

LightingWindow* makeLightingWindow() {
  LOG(INFO) << "About to take mml";
  MessageManagerLock l;
  LOG(INFO) << "mml taken";

  auto window = make_unique<LightingWindow>();
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

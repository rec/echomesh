#include "Tiny.h"

#include "JuceHeader.h"

using namespace echomesh;
using namespace juce;
using namespace std;

namespace echomesh {

namespace {

class TinyWindow : public DocumentWindow {
 public:
  TinyWindow() : DocumentWindow("echomesh lighting simulator",
                                Colours::lightgrey,
                                DocumentWindow::allButtons) {
    setUsingNativeTitleBar(true);
    setSize(200, 200);
    toFront(true);
  }

  void closeButtonPressed() {
    cout << "CLOSE\n";
  }
};

ScopedPointer<TinyWindow> tinyWindow;

}  // namespace

void Tiny::show() {
  tinyWindow = new TinyWindow;
}

void Tiny::hide() {
  tinyWindow = NULL;
}

}  // namespace echomesh

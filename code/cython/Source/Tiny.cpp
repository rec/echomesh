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
    cout << "first\n";
    // setUsingNativeTitleBar(true);
    cout << "second\n";
    setSize(200, 200);
    cout << "third\n";
    toFront(true);
    setVisible(true);
    cout << "fourth\n";
  }

  void closeButtonPressed() {
    cout << "CLOSE\n";
  }
};

ScopedPointer<TinyWindow> tinyWindow;

}  // namespace

void Tiny::show() {
  cout << "zeroth\n";
  tinyWindow = new TinyWindow;
}

void Tiny::hide() {
  tinyWindow = NULL;
}

}  // namespace echomesh

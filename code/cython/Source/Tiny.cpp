#include "Tiny.h"

#include "JuceHeader.h"
#include "echomesh/EchomeshApplication.h"

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
  echomesh::startEchomesh();
  cout << "0.5\n";
  tinyWindow = new TinyWindow;
}

void Tiny::hide() {
  tinyWindow = NULL;
}

}  // namespace echomesh

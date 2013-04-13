# Not general, will probably on work on my Mac.  :-)

all:

clean:
	find . -name \*.pyc | xargs rm
	rm TAGS

tags:
	find . -name \*.py | xargs etags

ROOT := /development/echomesh/
BUILD_ROOT := $(ROOT)code/cpp/echomesh/Builds/MacOSX/
RELEASE_EXECUTABLE := $(BUILD_ROOT)build/Release/echomesh.app/Contents/MacOS/echomesh
DEBUG_EXECUTABLE := $(BUILD_ROOT)build/Debug/echomesh.app/Contents/MacOS/echomesh
BIN := $(ROOT)bin/darwin/

debug:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh.xcodeproj" -configuration Debug
	cp $(DEBUG_EXECUTABLE) $(BIN)

release:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh.xcodeproj" -configuration Release
	cp $(RELEASE_EXECUTABLE) $(BIN)


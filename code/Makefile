# Not general, will probably on work on my Mac.  :-)

all:

clean:
	find . -name \*.pyc | xargs rm
	rm TAGS

tags:
	find . -name \*.py | xargs etags

ROOT := /development/echomesh/
BUILD_ROOT := $(ROOT)code/cpp/Builds/MacOSX/
RELEASE_EXECUTABLE := $(BUILD_ROOT)build/Release/echomesh-client.app/Contents/MacOS/echomesh-client
DEBUG_EXECUTABLE := $(BUILD_ROOT)build/Debug/echomesh-client.app/Contents/MacOS/echomesh-client
BIN := $(ROOT)bin/darwin/

debug:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh-client.xcodeproj" -configuration Debug

release:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh-client.xcodeproj" -configuration Release

debug_deploy: debug
	cp $(DEBUG_EXECUTABLE) $(BIN)

release_deploy: release
	cp $(RELEASE_EXECUTABLE) $(BIN)


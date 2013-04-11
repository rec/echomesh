all:

clean:
	find . -name \*.pyc | xargs rm
	rm TAGS

tags:
	find . -name \*.py | xargs etags

ROOT := /development/echomesh
BUILD_ROOT := $(ROOT)/code/cpp/echomesh/Builds/MacOSX

debug:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh.xcodeproj" -configuration Debug

release:
	cd $(BUILD_ROOT) && xcodebuild -project "echomesh.xcodeproj" -configuration Release


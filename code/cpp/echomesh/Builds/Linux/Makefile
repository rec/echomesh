# Automatically generated makefile, created by the Introjucer
# Don't edit this file! Your changes will be overwritten when you re-save the Introjucer project!

ifndef CONFIG
  CONFIG=Debug
endif

ifeq ($(TARGET_ARCH),)
  TARGET_ARCH := -march=native
endif

# (this disables dependency generation if multiple architectures are set)
DEPFLAGS := $(if $(word 2, $(TARGET_ARCH)), , -MMD)

ifeq ($(CONFIG),Debug)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Debug
  OUTDIR := build
  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -g -ggdb -O0
  CXXFLAGS += $(CFLAGS) 
  LDFLAGS += -L$(BINDIR) -L$(LIBDIR) -L/usr/X11R6/lib/ -lGL -lX11 -lXext -lXinerama -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  TARGET := echomesh
  BLDCMD = $(CXX) -o $(OUTDIR)/$(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(TARGET_ARCH)
endif

ifeq ($(CONFIG),Release)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Release
  OUTDIR := build
  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "NDEBUG=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -Os
  CXXFLAGS += $(CFLAGS) 
  LDFLAGS += -L$(BINDIR) -L$(LIBDIR) -L/usr/X11R6/lib/ -lGL -lX11 -lXext -lXinerama -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "NDEBUG=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  TARGET := echomesh
  BLDCMD = $(CXX) -o $(OUTDIR)/$(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(TARGET_ARCH)
endif

OBJECTS := \
  $(OBJDIR)/LightComponent_f5f4d090.o \
  $(OBJDIR)/ReadThread_a8da40c9.o \
  $(OBJDIR)/aliascontent_8112a045.o \
  $(OBJDIR)/aliasmanager_9a9bc179.o \
  $(OBJDIR)/content_c501d867.o \
  $(OBJDIR)/conversion_4a091072.o \
  $(OBJDIR)/directives_a07ca660.o \
  $(OBJDIR)/emitfromevents_9dcfb532.o \
  $(OBJDIR)/emitter_2ae7dcdc.o \
  $(OBJDIR)/emitterstate_3e6d4cff.o \
  $(OBJDIR)/emitterutils_146891f.o \
  $(OBJDIR)/exp_9b3e808b.o \
  $(OBJDIR)/iterator_cbbb258a.o \
  $(OBJDIR)/map_1b30e44a.o \
  $(OBJDIR)/node_85d8ac9e.o \
  $(OBJDIR)/nodebuilder_39278ac7.o \
  $(OBJDIR)/null_d14779a3.o \
  $(OBJDIR)/ostream_2426999d.o \
  $(OBJDIR)/parser_30ac467b.o \
  $(OBJDIR)/parserstate_6f550ec0.o \
  $(OBJDIR)/regex_1a301775.o \
  $(OBJDIR)/scalar_d6fe7bc8.o \
  $(OBJDIR)/scanner_75bb4f6c.o \
  $(OBJDIR)/scanscalar_13ca1e85.o \
  $(OBJDIR)/scantag_abb24deb.o \
  $(OBJDIR)/scantoken_689749ca.o \
  $(OBJDIR)/sequence_dc71b35d.o \
  $(OBJDIR)/simplekey_c9b8371b.o \
  $(OBJDIR)/singledocparser_fc89e3fd.o \
  $(OBJDIR)/stream_22ebc15c.o \
  $(OBJDIR)/tag_8cfdaf88.o \
  $(OBJDIR)/Main_90ebc5c2.o \
  $(OBJDIR)/juce_core_aff681cc.o \
  $(OBJDIR)/juce_cryptography_25c7e826.o \
  $(OBJDIR)/juce_data_structures_bdd6d488.o \
  $(OBJDIR)/juce_events_79b2840.o \
  $(OBJDIR)/juce_graphics_c8f1e7a4.o \
  $(OBJDIR)/juce_gui_basics_a630dd20.o \
  $(OBJDIR)/juce_gui_extra_7767d6a8.o \
  $(OBJDIR)/juce_opengl_c7e3506c.o \
  $(OBJDIR)/juce_video_184321c8.o \

.PHONY: clean

$(OUTDIR)/$(TARGET): $(OBJECTS) $(LDDEPS) $(RESOURCES)
	@echo Linking echomesh
	-@mkdir -p $(BINDIR)
	-@mkdir -p $(LIBDIR)
	-@mkdir -p $(OUTDIR)
	@$(BLDCMD)

clean:
	@echo Cleaning echomesh
	-@rm -f $(OUTDIR)/$(TARGET)
	-@rm -rf $(OBJDIR)/*
	-@rm -rf $(OBJDIR)

strip:
	@echo Stripping echomesh
	-@strip --strip-unneeded $(OUTDIR)/$(TARGET)

$(OBJDIR)/LightComponent_f5f4d090.o: ../../Source/LightComponent.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling LightComponent.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ReadThread_a8da40c9.o: ../../Source/ReadThread.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ReadThread.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/aliascontent_8112a045.o: ../../Source/yaml-cpp-src/aliascontent.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling aliascontent.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/aliasmanager_9a9bc179.o: ../../Source/yaml-cpp-src/aliasmanager.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling aliasmanager.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/content_c501d867.o: ../../Source/yaml-cpp-src/content.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling content.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/conversion_4a091072.o: ../../Source/yaml-cpp-src/conversion.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling conversion.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/directives_a07ca660.o: ../../Source/yaml-cpp-src/directives.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling directives.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitfromevents_9dcfb532.o: ../../Source/yaml-cpp-src/emitfromevents.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitfromevents.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitter_2ae7dcdc.o: ../../Source/yaml-cpp-src/emitter.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitter.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitterstate_3e6d4cff.o: ../../Source/yaml-cpp-src/emitterstate.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitterstate.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitterutils_146891f.o: ../../Source/yaml-cpp-src/emitterutils.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitterutils.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/exp_9b3e808b.o: ../../Source/yaml-cpp-src/exp.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling exp.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/iterator_cbbb258a.o: ../../Source/yaml-cpp-src/iterator.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling iterator.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/map_1b30e44a.o: ../../Source/yaml-cpp-src/map.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling map.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/node_85d8ac9e.o: ../../Source/yaml-cpp-src/node.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling node.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/nodebuilder_39278ac7.o: ../../Source/yaml-cpp-src/nodebuilder.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling nodebuilder.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/null_d14779a3.o: ../../Source/yaml-cpp-src/null.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling null.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ostream_2426999d.o: ../../Source/yaml-cpp-src/ostream.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ostream.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/parser_30ac467b.o: ../../Source/yaml-cpp-src/parser.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling parser.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/parserstate_6f550ec0.o: ../../Source/yaml-cpp-src/parserstate.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling parserstate.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/regex_1a301775.o: ../../Source/yaml-cpp-src/regex.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling regex.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scalar_d6fe7bc8.o: ../../Source/yaml-cpp-src/scalar.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scalar.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scanner_75bb4f6c.o: ../../Source/yaml-cpp-src/scanner.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scanner.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scanscalar_13ca1e85.o: ../../Source/yaml-cpp-src/scanscalar.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scanscalar.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scantag_abb24deb.o: ../../Source/yaml-cpp-src/scantag.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scantag.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scantoken_689749ca.o: ../../Source/yaml-cpp-src/scantoken.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scantoken.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/sequence_dc71b35d.o: ../../Source/yaml-cpp-src/sequence.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling sequence.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/simplekey_c9b8371b.o: ../../Source/yaml-cpp-src/simplekey.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling simplekey.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/singledocparser_fc89e3fd.o: ../../Source/yaml-cpp-src/singledocparser.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling singledocparser.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/stream_22ebc15c.o: ../../Source/yaml-cpp-src/stream.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling stream.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/tag_8cfdaf88.o: ../../Source/yaml-cpp-src/tag.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling tag.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Main_90ebc5c2.o: ../../Source/Main.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Main.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_core_aff681cc.o: ../../JuceLibraryCode/modules/juce_core/juce_core.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_core.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_cryptography_25c7e826.o: ../../JuceLibraryCode/modules/juce_cryptography/juce_cryptography.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_cryptography.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_data_structures_bdd6d488.o: ../../JuceLibraryCode/modules/juce_data_structures/juce_data_structures.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_data_structures.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_events_79b2840.o: ../../JuceLibraryCode/modules/juce_events/juce_events.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_events.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_graphics_c8f1e7a4.o: ../../JuceLibraryCode/modules/juce_graphics/juce_graphics.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_graphics.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_gui_basics_a630dd20.o: ../../JuceLibraryCode/modules/juce_gui_basics/juce_gui_basics.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_gui_basics.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_gui_extra_7767d6a8.o: ../../JuceLibraryCode/modules/juce_gui_extra/juce_gui_extra.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_gui_extra.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_opengl_c7e3506c.o: ../../JuceLibraryCode/modules/juce_opengl/juce_opengl.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_opengl.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_video_184321c8.o: ../../JuceLibraryCode/modules/juce_video/juce_video.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_video.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

-include $(OBJECTS:%.o=%.d)

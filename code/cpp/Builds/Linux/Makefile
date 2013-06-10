# Automatically generated makefile, created by the Introjucer
# Don't edit this file! Your changes will be overwritten when you re-save the Introjucer project!

ifndef CONFIG
  CONFIG=Debug
endif

ifeq ($(CONFIG),Debug)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Debug
  OUTDIR := build

  ifeq ($(TARGET_ARCH),)
    TARGET_ARCH := -march=armv6
  endif

  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCE_USE_XSHM=0" -D "JUCE_USE_XINERAMA=0" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -g -ggdb -O0
  CXXFLAGS += $(CFLAGS) -I../..
  LDFLAGS += $(TARGET_ARCH) -L$(BINDIR) -L$(LIBDIR) -L/usr/X11R6/lib/ -lGL -lX11 -lXext -lXinerama -lasound -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCE_USE_XSHM=0" -D "JUCE_USE_XINERAMA=0" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  TARGET := echomesh-client
  BLDCMD = $(CXX) -o $(OUTDIR)/$(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(TARGET_ARCH)
endif

ifeq ($(CONFIG),Release)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Release
  OUTDIR := build

  ifeq ($(TARGET_ARCH),)
    TARGET_ARCH := -march=armv6
  endif

  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "NDEBUG=1" -D "JUCE_USE_XSHM=0" -D "JUCE_USE_XINERAMA=0" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -Os
  CXXFLAGS += $(CFLAGS) -I../..
  LDFLAGS += $(TARGET_ARCH) -L$(BINDIR) -L$(LIBDIR) -L/usr/X11R6/lib/ -lGL -lX11 -lXext -lXinerama -lasound -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "NDEBUG=1" -D "JUCE_USE_XSHM=0" -D "JUCE_USE_XINERAMA=0" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode
  TARGET := echomesh-client
  BLDCMD = $(CXX) -o $(OUTDIR)/$(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(TARGET_ARCH)
endif

# (this disables dependency generation if multiple architectures are set)
DEPFLAGS := $(if $(word 2, $(TARGET_ARCH)), , -MMD)

OBJECTS := \
  $(OBJDIR)/GetDevice_bdff9491.o \
  $(OBJDIR)/Config_4a6afa38.o \
  $(OBJDIR)/Log_edbe3e58.o \
  $(OBJDIR)/InstrumentComponent_75edd5bc.o \
  $(OBJDIR)/InstrumentGrid_18eea031.o \
  $(OBJDIR)/LightingWindow_79bb5b00.o \
  $(OBJDIR)/Main_ed86ae4b.o \
  $(OBJDIR)/LightReader_649349d0.o \
  $(OBJDIR)/LineGetter_4e1cc2f2.o \
  $(OBJDIR)/ReadThread_1a08d793.o \
  $(OBJDIR)/SocketLineGetter_649dfac5.o \
  $(OBJDIR)/base64_1eb4a3a4.o \
  $(OBJDIR)/RealTime_4c146fff.o \
  $(OBJDIR)/Trash_ed189496.o \
  $(OBJDIR)/aliascontent_51f9ebd9.o \
  $(OBJDIR)/aliasmanager_6b830d0d.o \
  $(OBJDIR)/content_2bb6a053.o \
  $(OBJDIR)/conversion_51b63106.o \
  $(OBJDIR)/directives_a829c6f4.o \
  $(OBJDIR)/emitfromevents_d2126bc6.o \
  $(OBJDIR)/emitter_919ca4c8.o \
  $(OBJDIR)/emitterstate_f549893.o \
  $(OBJDIR)/emitterutils_d22dd4b3.o \
  $(OBJDIR)/exp_ff0c1e77.o \
  $(OBJDIR)/iterator_3b9f5b1e.o \
  $(OBJDIR)/map_7efe8236.o \
  $(OBJDIR)/node_9bbecc32.o \
  $(OBJDIR)/nodebuilder_271e7cb3.o \
  $(OBJDIR)/null_e72d9937.o \
  $(OBJDIR)/ostream_8adb6189.o \
  $(OBJDIR)/parser_6588d10f.o \
  $(OBJDIR)/parserstate_5d4c00ac.o \
  $(OBJDIR)/regex_c10dea61.o \
  $(OBJDIR)/scalar_bdb065c.o \
  $(OBJDIR)/scanner_dc701758.o \
  $(OBJDIR)/scanscalar_1b773f19.o \
  $(OBJDIR)/scantag_126715d7.o \
  $(OBJDIR)/scantoken_f539c6b6.o \
  $(OBJDIR)/sequence_4c55e8f1.o \
  $(OBJDIR)/simplekey_565ab407.o \
  $(OBJDIR)/singledocparser_509dffe9.o \
  $(OBJDIR)/stream_57c84bf0.o \
  $(OBJDIR)/tag_f0cb4d74.o \
  $(OBJDIR)/juce_audio_basics_2442e4ea.o \
  $(OBJDIR)/juce_audio_devices_a4c8a728.o \
  $(OBJDIR)/juce_audio_formats_d349f0c8.o \
  $(OBJDIR)/juce_audio_processors_44a134a2.o \
  $(OBJDIR)/juce_audio_utils_f63b12e8.o \
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
	@echo Linking echomesh-client
	-@mkdir -p $(BINDIR)
	-@mkdir -p $(LIBDIR)
	-@mkdir -p $(OUTDIR)
	@$(BLDCMD)

clean:
	@echo Cleaning echomesh-client
	-@rm -f $(OUTDIR)/$(TARGET)
	-@rm -rf $(OBJDIR)/*
	-@rm -rf $(OBJDIR)

strip:
	@echo Stripping echomesh-client
	-@strip --strip-unneeded $(OUTDIR)/$(TARGET)

$(OBJDIR)/GetDevice_bdff9491.o: ../../echomesh/util/GetDevice.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling GetDevice.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Config_4a6afa38.o: ../../echomesh/base/Config.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Config.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Log_edbe3e58.o: ../../echomesh/base/Log.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Log.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/InstrumentComponent_75edd5bc.o: ../../echomesh/component/InstrumentComponent.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling InstrumentComponent.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/InstrumentGrid_18eea031.o: ../../echomesh/component/InstrumentGrid.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling InstrumentGrid.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/LightingWindow_79bb5b00.o: ../../echomesh/component/LightingWindow.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling LightingWindow.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Main_ed86ae4b.o: ../../echomesh/Main.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Main.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/LightReader_649349d0.o: ../../echomesh/network/LightReader.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling LightReader.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/LineGetter_4e1cc2f2.o: ../../echomesh/network/LineGetter.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling LineGetter.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ReadThread_1a08d793.o: ../../echomesh/network/ReadThread.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ReadThread.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/SocketLineGetter_649dfac5.o: ../../echomesh/network/SocketLineGetter.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling SocketLineGetter.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/base64_1eb4a3a4.o: ../../base64/base64.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling base64.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/RealTime_4c146fff.o: ../../rec/base/RealTime.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling RealTime.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Trash_ed189496.o: ../../rec/util/thread/Trash.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Trash.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/aliascontent_51f9ebd9.o: ../../yaml-cpp-src/aliascontent.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling aliascontent.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/aliasmanager_6b830d0d.o: ../../yaml-cpp-src/aliasmanager.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling aliasmanager.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/content_2bb6a053.o: ../../yaml-cpp-src/content.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling content.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/conversion_51b63106.o: ../../yaml-cpp-src/conversion.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling conversion.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/directives_a829c6f4.o: ../../yaml-cpp-src/directives.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling directives.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitfromevents_d2126bc6.o: ../../yaml-cpp-src/emitfromevents.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitfromevents.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitter_919ca4c8.o: ../../yaml-cpp-src/emitter.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitter.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitterstate_f549893.o: ../../yaml-cpp-src/emitterstate.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitterstate.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/emitterutils_d22dd4b3.o: ../../yaml-cpp-src/emitterutils.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling emitterutils.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/exp_ff0c1e77.o: ../../yaml-cpp-src/exp.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling exp.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/iterator_3b9f5b1e.o: ../../yaml-cpp-src/iterator.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling iterator.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/map_7efe8236.o: ../../yaml-cpp-src/map.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling map.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/node_9bbecc32.o: ../../yaml-cpp-src/node.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling node.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/nodebuilder_271e7cb3.o: ../../yaml-cpp-src/nodebuilder.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling nodebuilder.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/null_e72d9937.o: ../../yaml-cpp-src/null.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling null.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ostream_8adb6189.o: ../../yaml-cpp-src/ostream.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ostream.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/parser_6588d10f.o: ../../yaml-cpp-src/parser.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling parser.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/parserstate_5d4c00ac.o: ../../yaml-cpp-src/parserstate.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling parserstate.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/regex_c10dea61.o: ../../yaml-cpp-src/regex.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling regex.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scalar_bdb065c.o: ../../yaml-cpp-src/scalar.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scalar.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scanner_dc701758.o: ../../yaml-cpp-src/scanner.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scanner.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scanscalar_1b773f19.o: ../../yaml-cpp-src/scanscalar.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scanscalar.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scantag_126715d7.o: ../../yaml-cpp-src/scantag.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scantag.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/scantoken_f539c6b6.o: ../../yaml-cpp-src/scantoken.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling scantoken.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/sequence_4c55e8f1.o: ../../yaml-cpp-src/sequence.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling sequence.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/simplekey_565ab407.o: ../../yaml-cpp-src/simplekey.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling simplekey.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/singledocparser_509dffe9.o: ../../yaml-cpp-src/singledocparser.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling singledocparser.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/stream_57c84bf0.o: ../../yaml-cpp-src/stream.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling stream.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/tag_f0cb4d74.o: ../../yaml-cpp-src/tag.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling tag.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_audio_basics_2442e4ea.o: ../../JuceLibraryCode/modules/juce_audio_basics/juce_audio_basics.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_audio_basics.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_audio_devices_a4c8a728.o: ../../JuceLibraryCode/modules/juce_audio_devices/juce_audio_devices.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_audio_devices.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_audio_formats_d349f0c8.o: ../../JuceLibraryCode/modules/juce_audio_formats/juce_audio_formats.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_audio_formats.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_audio_processors_44a134a2.o: ../../JuceLibraryCode/modules/juce_audio_processors/juce_audio_processors.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_audio_processors.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/juce_audio_utils_f63b12e8.o: ../../JuceLibraryCode/modules/juce_audio_utils/juce_audio_utils.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling juce_audio_utils.cpp"
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

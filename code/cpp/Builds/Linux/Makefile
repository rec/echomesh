# Automatically generated makefile, created by the Introjucer
# Don't edit this file! Your changes will be overwritten when you re-save the Introjucer project!

# (this disables dependency generation if multiple architectures are set)
DEPFLAGS := $(if $(word 2, $(TARGET_ARCH)), , -MMD)

ifndef CONFIG
  CONFIG=Debug
endif

ifeq ($(CONFIG),Debug)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Debug
  OUTDIR := build

  ifeq ($(TARGET_ARCH),)
    TARGET_ARCH := -march=native
  endif

  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCE_DISABLE_JUCE_VERSION_PRINTING=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode -I ../../JuceLibraryCode/modules
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -g -ggdb -O0 -I../..  -std=c++11
  CXXFLAGS += $(CFLAGS)
  LDFLAGS += $(TARGET_ARCH) -L$(BINDIR) -L$(LIBDIR) -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "DEBUG=1" -D "_DEBUG=1" -D "JUCE_DISABLE_JUCE_VERSION_PRINTING=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode -I ../../JuceLibraryCode/modules
  TARGET := libechomesh.a
  BLDCMD = ar -rcs $(OUTDIR)/$(TARGET) $(OBJECTS)
endif

ifeq ($(CONFIG),Release)
  BINDIR := build
  LIBDIR := build
  OBJDIR := build/intermediate/Release
  OUTDIR := build

  ifeq ($(TARGET_ARCH),)
    TARGET_ARCH := -march=native
  endif

  CPPFLAGS := $(DEPFLAGS) -D "LINUX=1" -D "NDEBUG=1" -D "JUCE_DISABLE_JUCE_VERSION_PRINTING=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode -I ../../JuceLibraryCode/modules
  CFLAGS += $(CPPFLAGS) $(TARGET_ARCH) -Os -I../..  -std=c++11
  CXXFLAGS += $(CFLAGS)
  LDFLAGS += $(TARGET_ARCH) -L$(BINDIR) -L$(LIBDIR) -fvisibility=hidden -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound -ldl -lfreetype -lpthread -lrt 
  LDDEPS :=
  RESFLAGS :=  -D "LINUX=1" -D "NDEBUG=1" -D "JUCE_DISABLE_JUCE_VERSION_PRINTING=1" -D "JUCER_LINUX_MAKE_7346DA2A=1" -I /usr/include -I /usr/include/freetype2 -I ../../JuceLibraryCode -I ../../JuceLibraryCode/modules
  TARGET := libechomesh.a
  BLDCMD = ar -rcs $(OUTDIR)/$(TARGET) $(OBJECTS)
endif

OBJECTS := \
  $(OBJDIR)/AudioPlayer_4a16e216.o \
  $(OBJDIR)/DefaultDevice_d5d51936.o \
  $(OBJDIR)/Envelope_e091de3b.o \
  $(OBJDIR)/EnvelopePlayer_6908c03c.o \
  $(OBJDIR)/GetReader_4ae00cf8.o \
  $(OBJDIR)/MidiController_f87aad08.o \
  $(OBJDIR)/PanGainPlayer_d877dfc.o \
  $(OBJDIR)/ResamplingPositionableAudioSource_55438ad3.o \
  $(OBJDIR)/SampleAudioSource_602b6bc6.o \
  $(OBJDIR)/Source_b9c08e86.o \
  $(OBJDIR)/InstrumentComponent_75edd5bc.o \
  $(OBJDIR)/InstrumentGrid_18eea031.o \
  $(OBJDIR)/LightingWindow_79bb5b00.o \
  $(OBJDIR)/ColorModel_26f43044.o \
  $(OBJDIR)/ColorName_ff26ac1a.o \
  $(OBJDIR)/HSB_7615b903.o \
  $(OBJDIR)/Transform_d1c2c3f8.o \
  $(OBJDIR)/InitLog_83a5ff59.o \
  $(OBJDIR)/EchomeshApplication_68207ea3.o \
  $(OBJDIR)/FastTrig_b97710bd.o \
  $(OBJDIR)/Quit_38fc84f4.o \
  $(OBJDIR)/Manager_ac61fac2.o \
  $(OBJDIR)/RegisterFormats_a3caa84e.o \
  $(OBJDIR)/OutputSampleRate_b96311f8.o \
  $(OBJDIR)/Trash_ed189496.o \
  $(OBJDIR)/juce_audio_basics_2442e4ea.o \
  $(OBJDIR)/juce_audio_devices_a4c8a728.o \
  $(OBJDIR)/juce_audio_formats_d349f0c8.o \
  $(OBJDIR)/juce_core_aff681cc.o \
  $(OBJDIR)/juce_cryptography_25c7e826.o \
  $(OBJDIR)/juce_data_structures_bdd6d488.o \
  $(OBJDIR)/juce_events_79b2840.o \
  $(OBJDIR)/juce_graphics_c8f1e7a4.o \
  $(OBJDIR)/juce_gui_basics_a630dd20.o \
  $(OBJDIR)/juce_gui_extra_7767d6a8.o \

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

$(OBJDIR)/AudioPlayer_4a16e216.o: ../../echomesh/audio/AudioPlayer.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling AudioPlayer.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/DefaultDevice_d5d51936.o: ../../echomesh/audio/DefaultDevice.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling DefaultDevice.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Envelope_e091de3b.o: ../../echomesh/audio/Envelope.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Envelope.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/EnvelopePlayer_6908c03c.o: ../../echomesh/audio/EnvelopePlayer.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling EnvelopePlayer.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/GetReader_4ae00cf8.o: ../../echomesh/audio/GetReader.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling GetReader.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/MidiController_f87aad08.o: ../../echomesh/audio/MidiController.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling MidiController.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/PanGainPlayer_d877dfc.o: ../../echomesh/audio/PanGainPlayer.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling PanGainPlayer.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ResamplingPositionableAudioSource_55438ad3.o: ../../echomesh/audio/ResamplingPositionableAudioSource.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ResamplingPositionableAudioSource.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/SampleAudioSource_602b6bc6.o: ../../echomesh/audio/SampleAudioSource.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling SampleAudioSource.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Source_b9c08e86.o: ../../echomesh/audio/Source.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Source.cpp"
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

$(OBJDIR)/ColorModel_26f43044.o: ../../echomesh/color/ColorModel.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ColorModel.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/ColorName_ff26ac1a.o: ../../echomesh/color/ColorName.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling ColorName.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/HSB_7615b903.o: ../../echomesh/color/HSB.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling HSB.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Transform_d1c2c3f8.o: ../../echomesh/color/Transform.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Transform.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/InitLog_83a5ff59.o: ../../echomesh/util/InitLog.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling InitLog.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/EchomeshApplication_68207ea3.o: ../../echomesh/util/EchomeshApplication.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling EchomeshApplication.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/FastTrig_b97710bd.o: ../../echomesh/util/FastTrig.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling FastTrig.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Quit_38fc84f4.o: ../../echomesh/util/Quit.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Quit.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Manager_ac61fac2.o: ../../rec/audio/format/Manager.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Manager.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/RegisterFormats_a3caa84e.o: ../../rec/audio/format/RegisterFormats.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling RegisterFormats.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/OutputSampleRate_b96311f8.o: ../../rec/audio/OutputSampleRate.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling OutputSampleRate.cpp"
	@$(CXX) $(CXXFLAGS) -o "$@" -c "$<"

$(OBJDIR)/Trash_ed189496.o: ../../rec/util/thread/Trash.cpp
	-@mkdir -p $(OBJDIR)
	@echo "Compiling Trash.cpp"
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

-include $(OBJECTS:%.o=%.d)

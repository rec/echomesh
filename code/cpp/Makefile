CFLAGS += -Wall
PROGRAM = Synth.bin
LDFLAGS = -lrt -lpthread -lglog
SOURCES = \
  Base.cpp \
  CallbackThread.cpp \
  Commands.cpp \
  Main.cpp \
  MakeTimerSpec.cpp \
  Owned.cpp \
  ProcessLine.cpp \
  Scheduler.cpp \
  ThreadPool.cpp \

LIGHT_PROGRAM = Lights
LIGHT_SOURCES = Lights.cpp

OBJECTS = $(SOURCES:.cpp=.o)
LIGHT_OBJECTS = $(LIGHT_SOURCES:.cpp=.o)

RM = rm -f

.cpp.o:
	$(CXX) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(LINK.cc) -o $@ $(OBJECTS)

$(LIGHT_PROGRAM): $(LIGHT_OBJECTS)
	$(LINK.cc) -o $@ $(LIGHT_OBJECTS)

clean:
	$(RM) $(PROGRAM) $(OBJECTS) make.out


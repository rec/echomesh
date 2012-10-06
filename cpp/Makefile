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


OBJECTS = $(SOURCES:.cpp=.o)
RM = rm -f

.cpp.o:
	$(CXX) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(LINK.cc) -o $@ $(OBJECTS)

clean:
	$(RM) $(PROGRAM) $(OBJECTS) make.out

CFLAGS += -Wall
PROGRAM = Synth.bin
LDFLAGS =
SOURCES = Main.cpp Commands.cpp ProcessLine.cpp MakeTimerSpec.cpp
OBJECTS = $(SOURCES:.cpp=.o)
RM = rm -f

.cpp.o:
	$(CXX) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(LINK.cc) -o $@ $(OBJECTS)

clean:
	$(RM) $(PROGRAM) $(OBJECTS) make.out

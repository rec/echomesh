CFLAGS += -Wall -DBSD_INTERFACE_FUNCTIONS
PROGRAM = Synth.bin
LDFLAGS =
SOURCES = Main.cpp Commands.cpp ProcessLine.cpp
OBJECTS = $(SOURCES:.c=.o)
RM = rm -f

#.c.o:
#	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(LINK.cc) -o $@ $(OBJECTS)

clean:
	$(RM) $(PROGRAM) $(OBJECTS) make.out

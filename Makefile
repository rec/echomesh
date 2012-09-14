PREPROCESS=gcc -E -C -x c -iquote ./src

# -E : Stop after preprocessing.
# -C : Don't discard comments.
# -x c : Treat the file as C code.
# -iquote ./src : Use ./src for the non-system include path.

TARGETS=targets/arduino/arduino.h targets/arduino/arduino.bin

all: $(TARGETS)

clean:
	rm $(TARGETS)

%.h: %.h.in src/*/*/*.h src/*/*/*.cpp
	$(PREPROCESS) $< -o $@

targets/arduino/arduino.bin: src/*/*/*.h src/*/*/*.cpp
	g++ -g -iquote ./targets -iquote ./src -iquote ./src/yaml $< -o $@
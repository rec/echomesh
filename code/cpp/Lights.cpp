#include <stdio.h>
#include <string.h>
#include <strings.h>

typedef unsigned char byte;

const char DEVICE_NAME[] = "/dev/spidev0.0";

const int LIGHT_COUNT = 240;
const int LATCH_BYTE_COUNT = 2;
const int REPEAT_COUNT = 2;
const int LIGHT_BYTE_COUNT = 3 * LIGHT_COUNT;
const int BYTE_COUNT = LIGHT_BYTE_COUNT + LATCH_BYTE_COUNT;

byte LIGHT_BYTES[BYTE_COUNT];

void write(FILE* file) {
  fwrite(LIGHT_BYTES, 1, sizeof(LIGHT_BYTES), file);
  fflush(file);
}

int main() {
  memset(LIGHT_BYTES, BYTE_COUNT, 0x80);
  bzero(LIGHT_BYTES + LIGHT_BYTE_COUNT, LATCH_BYTE_COUNT);
  FILE* file = fopen(DEVICE_NAME, "w");
  write(file);

  for (int i = 0; i < REPEAT_COUNT; ++i) {
    bool reverse = (i % 2);
    for (int j = 0; j < LIGHT_COUNT; ++j) {
      int index = 3 * (reverse ? (LIGHT_COUNT - j - 1) : j);
      memset(LIGHT_BYTES + index, 0xFF, 3);
      write(file);
      memset(LIGHT_BYTES + index, 0x80, 3);
    }
  }
}

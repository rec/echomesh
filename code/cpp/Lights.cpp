#include "stdio.h"

const char DEVICE_NAME[] = "/dev/spidev0.0";

int main() {
  FILE* f = fopen(DEVICE_NAME, "w");

}

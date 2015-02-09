#include <stdio.h>
#include "../src/unidecode.c"

int main() {
  char* in;
  char* out;
  size_t out_len;

  in = "Hello there!!!\0";
  unidecode(in, strlen(in), &out, &out_len);
  printf("Convert: %s -> %s\n", in, out);

  in = "\u041F\u0440\u0438\u0432\u0435\u0442!\0";
  unidecode(in, strlen(in), &out, &out_len);
  printf("Convert: %s -> %s\n", in, out);

  return 0;
}
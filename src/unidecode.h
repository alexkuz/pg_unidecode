#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <iconv.h>

#include "data.h"
#include "pos.h"

int unidecode(char* src, size_t src_len, char** dst, size_t* dst_len);
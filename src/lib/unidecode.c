#include "unidecode.h"

// https://gist.github.com/antonijn/9009746

static int is_valid_char(uint32_t ch)
{
  return ch != -1 && (ch < 0xd800 || ch > 0xdfff);
}

static int getch(uint8_t buf[], unsigned long *idx, size_t str_len, uint32_t *cp)
{
  int remunits;
  uint8_t nxt, msk;
  if (*idx >= str_len) {
    return -1;
  }
  nxt = buf[(*idx)++];
  if (nxt & 0x80) {
    msk = 0xe0;
    for (remunits = 1; (nxt & msk) != ((msk << 1) & 0xff); ++remunits) {
      msk = (msk >> 1) | 0x80;
      if (msk == 0xff) {
        return -1;
      }
    }
  } else {
    remunits = 0;
    msk = 0;
  }
  *cp = nxt & ~msk;
  while (remunits-- > 0) {
    *cp <<= 6;
    if (*idx >= str_len) {
      return -1;
    }
    *cp |= buf[(*idx)++] & 0x3f;
  }
  return 0;
}

static int utf8_to_utf32(uint8_t input[], uint32_t output[], size_t count,
                  size_t *out_size)
{
  unsigned long idx = 0;

  for (*out_size = 0; *out_size < count && idx < count; ++*out_size) {
    int i = (int) *out_size;
    getch(input, &idx, count, &output[i]);
    if (!is_valid_char(output[i])) {
      return -1;
    }
  }
  return 0;
}

int unidecode(char* src, size_t src_len, char** dst, size_t* dst_len) {
  size_t src_uni_len = (src_len + 1) * 4;
  int n = 0, start, end, i, res;
  uint32_t c, *src_uni, pos_len;

  pos_len = sizeof(pos) / sizeof(pos[0]);

  src_uni = palloc(src_uni_len);

  res = utf8_to_utf32((uint8_t*)src, src_uni, src_len, &src_uni_len);

  if (res == -1) {
    return -1;
  }

  *dst = palloc(src_uni_len * 10 + 1);

  for (i = 0; i < src_uni_len; ++i) {
    c = src_uni[i];

    if (c >= pos_len) {
      (*dst)[n] = '?';
      n++;
      continue;
    }

    start = pos[c];
    if (c == pos_len - 1) {
      end = start + 1;
    } else {
      end = pos[c + 1];
    }

    if (!start) {
      continue;
    }

    strncpy(*dst + n, chars + start, end - start);
    n += end - start;
  }

  pfree(src_uni);

  *dst_len = n;

  return 0;
}
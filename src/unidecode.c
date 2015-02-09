#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"

#include "lib/unidecode.c"

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

PG_FUNCTION_INFO_V1(pg_unidecode);

Datum
pg_unidecode(PG_FUNCTION_ARGS)
{
    text *arg1 = PG_GETARG_TEXT_P(0);
    char* out;
    size_t out_len;

    unidecode(VARDATA(arg1), VARSIZE(arg1) - VARHDRSZ, &out, &out_len);

    int new_text_size = VARHDRSZ + out_len;
    text* new_text = (text *) palloc(new_text_size);

    SET_VARSIZE(new_text, new_text_size);
    memcpy(VARDATA(new_text), out, out_len);

    free(out);
    PG_RETURN_TEXT_P(new_text);
}
MODULES := src/pg_unidecode
PG_CONFIG := pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
INCLUDEDIR := $(shell $(PG_CONFIG) --includedir-server)

include $(PGXS)

test: test/test
		test/test

src/data.h: builder/builder.py builder/unidecode/unidecode/*.py
		python builder/builder.py

test/test: test/test.c src/unidecode.c
		cc -liconv -o test/test test/test.c

src/pg_unidecode.so: src/pg_unidecode.o
		cc -bundle -flat_namespace -undefined suppress -o src/pg_unidecode.so src/pg_unidecode.o

src/pg_unidecode.o: src/pg_unidecode.c src/unidecode.c src/data.h
		cc -o src/pg_unidecode.o -c src/pg_unidecode.c $(CFLAGS) -I$(INCLUDEDIR)

.PHONY: test
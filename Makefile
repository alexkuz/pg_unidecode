EXTENSION    = $(shell grep -m 1 '"name":' META.json | \
               sed -e 's/[[:space:]]*"name":[[:space:]]*"\([^"]*\)",/\1/')
EXTVERSION   = $(shell grep -m 1 '[[:space:]]*"version":' META.json | \
               sed -e 's/[[:space:]]*"version":[[:space:]]*"\([^"]*\)",\{0,1\}/\1/')

DATA         = $(filter-out $(wildcard sql/*--*.sql),$(wildcard sql/*.sql))
# DOCS         = $(wildcard doc/*.mmd)
# TESTS        = $(wildcard test/sql/*.sql)
# REGRESS      = $(patsubst test/sql/%.sql,%,$(TESTS))
# REGRESS_OPTS = --inputdir=test --load-language=plpgsql
MODULES      = $(patsubst %.c,%,$(wildcard src/*.c))
PG_CONFIG   ?= pg_config
PG91         = $(shell $(PG_CONFIG) --version | grep -qE " 8\.| 9\.0" && echo no || echo yes)

CHARS_H      = src/data/chars.h
POS_H        = src/data/pos.h

ifeq ($(PG91),yes)
DATA = $(wildcard sql/*--*.sql)
EXTRA_CLEAN = sql/$(EXTENSION)--$(EXTVERSION).sql
endif

PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

ifeq ($(PG91),yes)
all: sql/$(EXTENSION)--$(EXTVERSION).sql $(CHARS_H) $(POS_H)

sql/$(EXTENSION)--$(EXTVERSION).sql: sql/$(EXTENSION).sql
	cp $< $@
else
all: $(CHARS_H) $(POS_H)
endif

dist:
	git archive --format zip --prefix=$(EXTENSION)-$(EXTVERSION)/ -o dist/$(EXTENSION)-$(EXTVERSION).zip HEAD

$(CHARS_H) $(POS_H): builder/builder.py builder/unidecode/unidecode/*.py
		python builder/builder.py
$(POS_H): $(CHARS_H)

CREATE OR REPLACE FUNCTION
  unidecode( TEXT )
RETURNS
  TEXT
AS
  'pg_unidecode.so', 'pg_unidecode'
LANGUAGE
  C
STRICT
IMMUTABLE;
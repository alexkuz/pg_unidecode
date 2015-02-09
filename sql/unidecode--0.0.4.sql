CREATE OR REPLACE FUNCTION
  unidecode( TEXT )
RETURNS
  TEXT
AS
  'unidecode.so', 'pg_unidecode'
LANGUAGE
  C
STRICT
IMMUTABLE;
pg_unidecode
============

This postgres extension is a port of [Unidecode](https://github.com/iki/unidecode) library, which provides ASCII transliteration of Unicode symbols:

    > SELECT unidecode('Français, Русский, 漢語 and English are my favorite languages') AS result;
                                 result                              
    -----------------------------------------------------------------
     Francais, Russkii, Han Yu  and English are my favorite languages
     
**NB**: this code is in early developing stage and I'm not that great at writing C code, so please don't use it in production yet!

Installation
------------

(I copypasted the following instructions from other project, so I'm not sure if everything will work as it said, but mostly it is valid)

To build it, just do this:

    make
    make installcheck
    make install

If you encounter an error such as:

    "Makefile", line 8: Need an operator

You need to use GNU make, which may well be installed on your system as
`gmake`:

    gmake
    gmake install
    gmake installcheck

If you encounter an error such as:

    make: pg_config: Command not found

Be sure that you have `pg_config` installed and in your path. If you used a
package management system such as RPM to install PostgreSQL, be sure that the
`-devel` package is also installed. If necessary tell the build process where
to find it:

    env PG_CONFIG=/path/to/pg_config make && make installcheck && make install

And finally, if all that fails (and if you're on PostgreSQL 8.1 or lower, it
likely will), copy the entire distribution directory to the `contrib/`
subdirectory of the PostgreSQL source tree and try it there without
`pg_config`:

    env NO_PGXS=1 make && make installcheck && make install

If you encounter an error such as:

    ERROR:  must be owner of database regression

You need to run the test suite using a super user, such as the default
"postgres" super user:

    make installcheck PGUSER=postgres
    
Once unidecode is installed, you can add it to a database. If you're running
PostgreSQL 9.1.0 or greater, it's a simple as connecting to a database as a
super user and running:

    CREATE EXTENSION unidecode;

If you've upgraded your cluster to PostgreSQL 9.1 and already had unidecode
installed, you can upgrade it to a properly packaged extension with:

    CREATE EXTENSION unidecode FROM unpackaged;

For versions of PostgreSQL less than 9.1.0, you'll need to run the
installation script:

    psql -d mydb -f /path/to/pgsql/share/contrib/unidecode.sql

If you want to install unidecode and all of its supporting objects into a specific
schema, use the `PGOPTIONS` environment variable to specify the schema, like
so:

    PGOPTIONS=--search_path=extensions psql -d mydb -f unidecode.sql

Dependencies
------------

You'll need PostgreSQL (obviously) and Python, if you are building it from git repo (or you can download last version with prebuilt data files from [PGXN](http://pgxn.org/dist/unidecode/))

Copyright
---------

COPYRIGHT

Copyright 2015, Alexander Kuznetsov <alexkuz@gmail.com>

This project uses transliteration tables from Python [Unidecode](https://github.com/iki/unidecode) library:

Original character transliteration tables:

Copyright 2001, Sean M. Burke <sburke@cpan.org>, all rights reserved.

Python code and later additions:

Copyright 2011, Tomaz Solc <tomaz@zemanta.com>

# -*- coding: utf-8 -*-
"""
Generates source data
"""
from __future__ import print_function

import imp
import os
import io
import re
import sys

DATA_DIR = os.environ.get("DATA_DIR")
UNIDECODE_REPOPATH = os.environ.get("UNIDECODE_REPOPATH")

if not DATA_DIR and UNIDECODE_REPOPATH:
    DATA_DIR = os.path.join(UNIDECODE_REPOPATH, "unidecode")

if not DATA_DIR:
    print("You must set the environment variable UNIDECODE_REPOPATH with the path of unidecode repository"
          ", cloned from https://github.com/avian2/unidecode", file=sys.stderr)
    sys.exit(2)


BUILD_DIR = 'src/data'

def create_data(data_file, pos_file):
    """
    create_data
    """
    data_file.write(u'char chars[] = "\\\n')
    pos_file.write(u'int pos[] = {\n')
    pos = 0

    ranges = {}
    for subdir, _, files in os.walk(DATA_DIR):
        ranges = {int(re.sub(r"(^x|\.py$)", "", filename), 16):
                  os.path.join(subdir, filename)
                  for filename in files
                  if filename.startswith('x') and
                     filename.endswith('py')}

    max_rng = max(ranges.keys())

    for rng in xrange(0, max_rng + 1):
        if rng != 0:
            pos_file.write(u',')

        if not rng in ranges:
            pos_file.write(u",".join([u"0" for i in xrange(0, 256)]))
            pos_file.write(u'\n')
            continue

        path = ranges[rng]

        module = imp.load_source('module', path)

        data_len = len(module.data)
        data = [module.data[i] if i < data_len else ''
                for i in xrange(0, 256)]
        for (i, char) in enumerate(data):
            charlen = len(char)

            char = char.replace('\\', '\\\\')
            char = ''.join([u'\\x%02x' % ord(c)
                    if ord(c) < 0x20
                    else c
                    for c in char])
            char = char.replace('"', '\\"')
            char = char.replace('%', '\\%')
            char = char.replace('?', '\\?')

            data_file.write(unicode(char))
            pos_file.write((u',%d' if i else u'%d') % pos)
            pos += charlen
        data_file.write(u'\\\n')
        pos_file.write(u'\n')
    data_file.write(u'";\n')
    pos_file.write(u'};\n')


def build():
    """
    build
    """
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    chars_path = os.path.join(BUILD_DIR, 'chars.h')
    pos_path = os.path.join(BUILD_DIR, 'pos.h')

    with io.open(chars_path, mode='w') as data_file:
        with io.open(pos_path, mode='w') as pos_file:
            create_data(data_file, pos_file)

build()

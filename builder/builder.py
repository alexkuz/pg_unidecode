# -*- coding: utf-8 -*-
"""
Generates source data
"""
import imp
import os
import io
import re

DATA_DIR = 'builder/unidecode/unidecode'

def create_data(data_file, pos_file):
    """
    create_data
    """
    data_file.write(u'char data[] = "\\\n')
    pos = 0

    ranges = {}
    for subdir, _, files in os.walk(DATA_DIR):
        ranges = {int(re.sub(r"(^x|\.py$)", "", filename), 16):
                  os.path.join(subdir, filename)
                  for filename in files
                  if filename.startswith('x') and
                     filename.endswith('py')}

    max_rng = max(ranges.keys())
    pos_file.write(u'int pos[%d][256] = {\n' % (max_rng + 1))

    for rng in xrange(0, max_rng + 1):
        pos_file.write(u'{' if rng == 0 else u',{')

        if not rng in ranges:
            pos_file.write(u",".join([u"0" for i in xrange(0, 256)]))
            pos_file.write(u'}\n')
            continue

        path = ranges[rng]

        module = imp.load_source('module', path)

        data_len = len(module.data)
        data = [module.data[i] if i < data_len else ''
                for i in xrange(0, 256)]
        for (i, char) in enumerate(data):
            charlen = len(char)

            char = char.replace('\\', '\\\\')
            char = ''.join([u'\\x%02d' % ord(c)
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
        pos_file.write(u'}\n')
    data_file.write(u'";\n')
    pos_file.write(u'};\n')


def build():
    """
    build
    """
    with io.open('src/data.h', mode='w') as data_file:
        with io.open('src/pos.h', mode='w') as pos_file:
            create_data(data_file, pos_file)

build()

#!/usr/bin/env python

#
# Realm667 - An Awesome Awesomeness
# Copyright (C) 2015 Alexey Lysiuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import pprint
import re
import sys


if len(sys.argv) < 2:
    print('Usage: {0} sndinfo.txt ...'.format(__file__))
    exit(1)

logical_sounds = set()
sound_lumps = set()

for filename in sys.argv[1:]:
    # Parse sndinfo.txt

    f = open(filename)
    content = f.read()
    f.close()

    content = re.sub(r'(//|;).*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    lines = content.split('\n')

    # TODO: avoid copy/paste from doomwad in parsing
    # TODO: add support for multi-line commands (with curly brackets)

    for line in lines:
        line = line.strip()

        if 0 == len(line):
            continue

        if line.startswith('$'):
            if line.lower().startswith(('$alias', '$random')):
                try:
                    _, logical, _ = line.split(None, 2)
                    logical_sounds.add("'{0}',\n".format(logical))
                except:
                    # ill-formed command, report error?
                    pass
            continue

        try:
            logical_name, lump_name = line.split()

            logical_name = logical_name.lower()
            lump_name = lump_name.upper()

            logical_sounds.add("'{0}',\n".format(logical_name))
            sound_lumps.add("'{0}',\n".format(lump_name))
        except:
            # ill-formed sound assignment, report error?
            pass

# Create header

self_path = os.path.dirname(__file__)
self_file = open(__file__)

header = []

while True:
    line = self_file.readline()

    if line.startswith('#'):
        header.append(line)
    else:
        break

self_file.close()

# Generate iwad_sndinfo.py

output_file = open(self_path + '/iwad_sndinfo.py', 'w')
output_file.writelines(header)
output_file.write('\nlogical_sounds_all = (\n')
output_file.writelines(sorted(logical_sounds))
output_file.write(')\n\nsounds_lumps_all = (\n')
output_file.writelines(sorted(sound_lumps))
output_file.write(')\n')
output_file.close()

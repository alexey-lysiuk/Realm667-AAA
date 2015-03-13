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

import collections
import os
import sys
import doomwad


if 2 != len(sys.argv):
    print('Usage: {} file.wad'.format(__file__))
    exit(1)

filename = sys.argv[1]

with open(filename, 'rb') as f:
    wad = doomwad.WadFile(f)

# find lump with palettes
lump = wad.find('PLAYPAL')
if not lump:
    print('Error: No palette found in {}'.format(filename))
    exit(1)

PALETTE_COLORS   = 256
PALETTE_CHANNELS = 3
PALETTE_BYTES    = PALETTE_COLORS * PALETTE_CHANNELS

if len(lump.data) < PALETTE_BYTES:
    print('Error: Invalid palette found in {}'.format(filename))
    exit(1)

# read first (normal) palette
colors = lump.data[:PALETTE_BYTES]
palette = []

for i in xrange(0, PALETTE_BYTES, 3):
    palette.append((
        ord(colors[i]),
        ord(colors[i + 1]),
        ord(colors[i + 2]),
        255))

for i in xrange(PALETTE_COLORS):
    rgb = palette[i]
    print('(0x%02X, 0x%02X, 0x%02X, 0xFF),' % (rgb[0], rgb[1], rgb[2]))

# find duplicate colors
duplicates = collections.defaultdict(list)

for index, rgb in enumerate(palette):
    duplicates[rgb].append(index)

print('\nDuplicate colors:')

for rgb, indices in sorted(duplicates.iteritems()):
    if len(indices) > 1:
        #print('{} -> {}'.format(rgb, indices))
        print('(0x%02X, 0x%02X, 0x%02X, 0xFF) -> %s'
            % (rgb[0], rgb[1], rgb[2], indices))

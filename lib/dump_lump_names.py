#!/usr/bin/env python

#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015 Alexey Lysiuk
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os, sys

sys.path.append(os.path.dirname(__file__))

import doomwad


if len(sys.argv) < 2:
    print('Usage: {0} file.wad'.format(__file__))
    exit(1)

# Scan WAD

wad_file = open(sys.argv[1])
wad = doomwad.WadFile(wad_file)

print('lumps = (')

for lump in wad.lumps:
    template = lump.marker and "# {0}" or  "'{0}',"
    print(template.format(lump.name))

print(')')

wad_file.close()

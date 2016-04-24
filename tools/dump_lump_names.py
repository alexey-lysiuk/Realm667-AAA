#!/usr/bin/env python

#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015, 2016 Alexey Lysiuk
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


import os
import re
import sys

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/../lib'

import doomwad


if len(sys.argv) < 2:
    print('Usage: {0} file.wad ...'.format(__file__))
    exit(1)


def skip_namespace(namespace):
    is_doom1_map = re.match(r'E\dM\d+', namespace)
    is_doom2_map = re.match(r'MAP\d+', namespace)

    sprite_marker = 'S_START'
    is_sprite = sprite_marker == namespace or sprite_marker == namespace[:1]

    return is_doom1_map or is_doom2_map or is_sprite


def dump_names(filename):
    wad_file = open(filename, 'rb')
    wad = doomwad.WadFile(wad_file)

    shortname = os.path.basename(filename).lower()
    shortname = shortname.split('.', 1)[0]

    print('lumps_{0} = ('.format(shortname))

    for namespace in wad.namespaces():
        if not skip_namespace(namespace):
            if len(namespace) > 0:
                print('# {0}'.format(namespace))

            lumps = wad.uniquenamespacelumps(namespace)
            lumps.sort(key = lambda lump: lump.name)

            for lump in lumps:
                if not lump.marker:
                    print("'{0}',".format(lump.name))

    print(')\n\nsprites_{0} = ('.format(shortname))

    for sprite in wad.spritenames():
        print("'{0}',".format(sprite))

    print(')\n')

    wad_file.close()


for filename in sys.argv[1:]:
    dump_names(filename)

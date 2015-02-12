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

import os
import re
import sys
import zipfile

self_path = os.path.dirname(__file__)
sys.path.append(self_path + '/lib')

import doomwad


zip_filename = self_path + '/../realm667-aaa.pk3'
zip_file = zipfile.ZipFile(zip_filename)

actors_wads = { }

def find_ammo_actors(wad_name, decorate, base_actor = 'Ammo'):
    ammo_pattern = r'\sactor\s+(\w+)\s*:\s+{0}'.format(base_actor)
    ammo_actors = re.findall(ammo_pattern, decorate, re.IGNORECASE)

    for actor in ammo_actors:
        if actor in actors_wads:
            actors_wads[actor].append(wad_name)
        else:
            actors_wads[actor] = [wad_name]

        find_ammo_actors(wad_name, decorate, actor)

for zipped_filename in zip_file.namelist():
    if not zipped_filename.lower().endswith('.wad'):
        continue

    # Scan WAD

    wad_file = zip_file.open(zipped_filename)
    wad_data = wad_file.read()
    wad_file.close()

    wad = doomwad.WadFile(wad_data)

    for lump in wad:
        if 'DECORATE' == lump.name:
            find_ammo_actors(zipped_filename, lump.data)

zip_file.close()

# Print names collisions

for actor in actors_wads:
    print('{0}: {1}'.format(actor, actors_wads[actor]))
    #print('    Command "{0}", "summon {0}"'.format(actor))

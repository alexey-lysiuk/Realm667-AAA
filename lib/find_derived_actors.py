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

import doomwad


def find_derived_actors(mapping, wad_name, decorate, base_actor):
    pattern = r'actor\s+([\w~.]+)\s*:\s+{0}'.format(base_actor)
    actors = re.findall(pattern, decorate, re.IGNORECASE)

    for actor in actors:
        if actor in mapping:
            mapping[actor].append(wad_name)
        else:
            mapping[actor] = [wad_name]

        find_derived_actors(mapping, wad_name, decorate, actor)

def print_result(mapping):
    for actor in mapping:
        print('{0}: {1}'.format(actor, mapping[actor]))
        #print('    Command "{0}", "summon {0}"'.format(actor))


zip_filename = os.path.dirname(__file__) + '/../realm667-aaa.pk3'
zip_file = zipfile.ZipFile(zip_filename)

ammo_actors_wads = { }
item_actors_wads = { }

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
            find_derived_actors(ammo_actors_wads, zipped_filename, \
                lump.data, 'Ammo')
            find_derived_actors(item_actors_wads, zipped_filename, \
                lump.data, 'CustomInventory')
            break

zip_file.close()

# Print names collisions

print('// Actors derived from Ammo:')
print_result(ammo_actors_wads)

print('\n// Actors derived from CustomInventory:')
print_result(item_actors_wads)

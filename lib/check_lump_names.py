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


'''
 This tool analyzes assets cache or generated .pk3
 for duplicate lump names within WAD files
 It prints result to stdout in 'known issues' markdown format
'''

import os, sys
import zipfile

self_path = os.path.dirname(__file__)
os.chdir(self_path)

import doomwad
from repo import excluded_wads
from lumps_iwads import lumps_ultdoom, lumps_doom2, lumps_tnt, lumps_plutonia, sprites_doom_all


excluded_lump_names = [
    'DECORATE',
    'KEYCONF',
    'SNDINFO',
    'DECALDEF',
    'GLDEFS',
    'LOADACS',
    'S_START',
    'S_END',
    'SS_START',
    'SS_END',
    '--------',
    'CREDITS',
    'INFO',
]

lumps_wads = { }
sprites_wads = { }


cache_path = '../cache/'

# Analyze cache if True and generated .pk3 if False
analyze_cache = False


# Scan cache or generated .pk3

zip_filenames = analyze_cache and os.listdir(cache_path) or ['../realm667-aaa.pk3']

for zip_filename in zip_filenames:
    zip_file = None

    if analyze_cache:
        zip_file = zipfile.ZipFile(cache_path + zip_filename)
        asset_id = int(zip_filename.replace('.zip', ''))
    else:
        zip_file = zipfile.ZipFile(zip_filename)

    for zipped_filename in zip_file.namelist():
        if not zipped_filename.lower().endswith('.wad'):
            continue

        # Check WAD for being excluded

        if analyze_cache:
            excluded = False

            for excluded_wad in excluded_wads:
                if id == excluded_wad[0] and zipped_filename == excluded_wad[1]:
                    excluded = True
                    break

            if excluded:
                continue

        # Scan WAD

        wad_file = zip_file.open(zipped_filename)
        wad_data = wad_file.read()
        wad_file.close()

        wad = doomwad.WadFile(wad_data)

        zip_wad = zipped_filename

        if analyze_cache:
            zip_wad = '[{:04d}] {:s}'.format(asset_id, zipped_filename)

        # Check all lumps except sprites

        for namespace in wad.namespaces():
            if doomwad.issrpitenamespace(namespace):
                continue

            for lump in wad.uniquenamespacelumps(namespace):
                if lump.name in excluded_lump_names:
                    continue

                if lump.name in lumps_wads:
                    lumps_wads[lump.name].append(zip_wad)
                else:
                    lumps_wads[lump.name] = [zip_wad]

        # Check sprites (4 characters names)

        for sprite in wad.spritenames():
            if sprite in sprites_wads:
                sprites_wads[sprite].append(zip_wad)
            else:
                sprites_wads[sprite] = [zip_wad]

    zip_file.close()

# Print names collisions

def print_duplicates(mapping, iwads):
    duplicates = []

    for name in mapping:
        wads = mapping[name]

        for iwad in iwads:
            if name in iwad[1]:
                wads.append(iwad[0])

        if 1 == len(wads):
            continue

        wads.sort(key = lambda name: name.lower())

        duplicates.append('|{0}|{1}||'.format(name, ', '.join(wads)))

    duplicates.sort()

    for dup in duplicates:
        print(dup)

print_duplicates(lumps_wads, (
    ('!DOOM.WAD',     lumps_ultdoom ),
    ('!DOOM2.WAD',    lumps_doom2   ),
    ('!TNT.WAD',      lumps_tnt     ),
    ('!PLUTONIA.WAD', lumps_plutonia),
))
print('')
print_duplicates(sprites_wads, (('!DOOM_ALL.WAD', sprites_doom_all),))

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


# This tool analyzes assets cache or generated .pk3
# for duplicate lump names within WAD files


import md5
import os, sys
import zipfile

self_path = os.path.dirname(__file__)
os.chdir(self_path)

import doomwad
from repo import excluded_wads


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

        for lump in wad.lumps:
            if not lump.name in excluded_lump_names:
                hash = md5.new()
                hash.update(lump.data)
                hash_str = hash.hexdigest()

                if lump.name in lumps_wads:
                    lumps_wads[lump.name][hash_str] = zip_wad
                else:
                    lumps_wads[lump.name] = {hash_str: zip_wad}

    zip_file.close()

# Print names collisions

for lump in lumps_wads:
    wads = lumps_wads[lump]

    if 1 == len(wads):
        continue

    filenames = ''

    for hash in wads:
        separator = len(filenames) > 0 and ', ' or ''
        filenames = '{0}{1}"{2}"'.format(filenames, separator, wads[hash])

    print('Different lumps with name {0} were found in {1} WADs: {2}'.format(lump, len(wads), filenames))

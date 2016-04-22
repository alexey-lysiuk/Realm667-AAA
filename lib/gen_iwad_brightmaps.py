#!/usr/bin/env python

#
# Realm667 - An Awesome Awesomeness
# Copyright (C) 2015, 2016 Alexey Lysiuk
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
import sys
import zipfile

import utils


if len(sys.argv) < 2:
    print('Usage: {0} brightmaps.pk3'.format(__file__))
    exit(1)

# Parse brightmaps.pk3 for names

pk3 = zipfile.ZipFile(sys.argv[1])
lumps = []

for zipped_filename in pk3.namelist():
    if not zipped_filename.lower().startswith('brightmaps/'):
        continue

    lump = os.path.basename(zipped_filename)
    lump = lump.rsplit('.', 1)[0].upper()

    lumps.append("('{0}'),\n".format(lump))

pk3.close()

# Generate iwad_brightmaps.py

output_file = open('iwad_brightmaps.py', 'w')
output_file.writelines(utils.license_header())
output_file.write('\nBRIGHTMAPS_ALL = (\n')
output_file.writelines(lumps)
output_file.write(')\n')
output_file.close()


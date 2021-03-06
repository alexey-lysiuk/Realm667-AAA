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
import zipfile

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/../lib'

import utils


if len(sys.argv) < 2:
    print('Usage: {0} (g)zdoom.pk3'.format(__file__))
    exit(1)

# Parse (g)zdoom.pk3 for actors

pk3 = zipfile.ZipFile(sys.argv[1])
content = []

for zipped_filename in pk3.namelist():
    if not zipped_filename.lower().startswith('actors/'):
        continue

    zipped_file = pk3.open(zipped_filename)
    zipped_data = utils.native_str(zipped_file.read())
    zipped_file.close()

    actor_pattern = r'actor\s+([\w+~.]+)(\s*:\s*[\w+~.]+)?'  \
        '(\s+replace\s+[\w+~.]+)?(\s+\d+)?(\s+native)?\s*{'
    actors = re.findall(actor_pattern, zipped_data, re.IGNORECASE)

    if len(actors) > 0:
        content.append('# {0}\n'.format(zipped_filename))

        for actor in actors:
            content.append("('{0}'),\n".format(actor[0]))

pk3.close()

# Generate actors_iwads.py

output_file = open(utils.lib_path() + 'iwad_actors.py', 'w')
output_file.writelines(utils.license_header())
output_file.write('\nACTORS_ALL = (\n')
output_file.writelines(content)
output_file.write(')\n')
output_file.close()

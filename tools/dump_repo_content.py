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
import sys
import shutil

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/../lib'

import repo
import utils

from web_repo import fetch_repository


remote_repo = fetch_repository()
toc = []

toc_path = utils.cache_path() + 'toc/'
shutil.rmtree(toc_path)
os.makedirs(toc_path)

outfile = None


def end_category():
    if outfile:
        outfile.write('\n[Back to table of content](../readme.md)\n')
        outfile.close()


for item in repo.content():
    gid = item[0]
    name = item[1]

    if 0 == gid:
        end_category()

        # start new category file by writing its header
        filename = name.replace(':', '').replace(' ', '-')
        filename = filename.replace('/', 'and').replace('&', 'and')
        filename = filename.lower() + '.md'
        outfile = open(toc_path + filename, 'w')

        outfile.write('####{}\n'.format(name))
        outfile.write('|ID|Name|Preview|Comment|\n|---|---|---|---|\n')

        toc.append('[{}](toc/{})  \n'.format(name, filename))
    else:
        # write asset row in the table
        abs_gid = abs(gid)

        url = 'https://github.com/alexey-lysiuk/Realm667-AAA-Cache/raw/master/'
        link = '[{0:d}]({1}{0:04d}.zip)'.format(abs_gid, url)

        preview = next((ri[3] for ri in remote_repo if abs_gid == ri[0]))
        preview = '![{}](http://www.realm667.com/{})'.format(name, preview)

        comment = ''

        if gid < 0:
            link = '~~' + link + '~~'
            name = '~~' + name + '~~'
            comment = 'Excluded from generated package'

        if outfile:
            outfile.write('|{}|{}|{}|{}|\n'.format(link, name, preview, comment))

end_category()

header = (
    '###Cache for Realm667 - An Awesome Awesomeness\n\n'
    'Git-based cache of assets from www.realm667.com repository used in '
    '[Realm667 - An Awesome Awesomeness]'
    '(https://github.com/alexey-lysiuk/Realm667-AAA) project.\n\n'
    '####Table of content\n'
)

with open(utils.cache_path() + 'readme.md', 'w') as outfile:
    outfile.write(header)
    outfile.writelines(toc)

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

from repo import REPOSITORY
from web_repo import fetch_repository

remote_repo = fetch_repository()

print('\n|ID|Name|Preview|Comment|\n|---|---|---|---|')

for item in REPOSITORY:
    gid = item[0]
    abs_gid = abs(gid)

    link = ''
    name = item[1]
    preview = ''
    comment = ''

    if 0 == gid:
        name = '**' + name + '**'
    else:
        url = 'https://github.com/alexey-lysiuk/Realm667-AAA-Cache/raw/master/'
        link = '[{0:d}]({1}{0:04d}.zip)'.format(abs_gid, url)
        preview = next((ri[3] for ri in remote_repo if abs_gid == ri[0]))
        preview = '![{}](http://www.realm667.com/{})'.format(name, preview)

        if gid < 0:
            link = '~~' + link + '~~'
            name = '~~' + name + '~~'
            comment = 'Excluded from generated package'

    print('|{}|{}|{}|{}|'.format(link, name, preview, comment))

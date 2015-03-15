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

from repo import repository

print('|ID|Name|Comment|\n|---|---|---|')

for item in repository:
    gid     = item[0]
    name    = item[1]

    if gid < 0:
        gid     = -gid
        comment = 'Excluded'
    else:
        comment = ''

    if 0 == gid:
        name = '**{}**'.format(name)
        link = ''
    else:
        link = '[{0:d}](https://github.com/alexey-lysiuk/Realm667-AAA-Cache/raw/master/{0:04d}.zip)'.format(gid)

    print('|{}|{}|{}|'.format(link, name, comment))

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
import urllib2


pattern_summon = re.compile('Summon:\s*(</strong>|</b>)\s*(\w[\w\s,-\.\(\)\']+)(<strong>|<b>|<br />)')
pattern_id_name = re.compile('gid=(\d+)"(\s+class="doclink")?>\s*(\w[\w\s,-\.\(\)\']+)\s*</a>')

repository = []


def fetch_repository(url):
    print('Fetching {0}'.format(url))

    response = urllib2.urlopen(url)
    html = response.read()

##    f = open('test.html', 'w')
##    f.write(html)
##    f.close

##    f = open('test.html', 'r')
##    html = f.read()
##    f.close()

    pos = 0

    while True:
        match = pattern_summon.search(html, pos)

        if not match:
            break

        summon = match.group(2)

        match = pattern_id_name.search(html, match.end())

        if not match:
            break

        id = match.group(1)
        name = match.group(3)

        repository.append([id, name, summon])

        pos = match.end()


url_armory_doom  = 'http://realm667.com/index.php/en/armory-mainmenu-157-97317/doom-style-mainmenu-158-94349?start={0}'
url_armory_hh    = 'http://realm667.com/index.php/en/armory-mainmenu-157-97317/heretic-hexen-style-mainmenu-159-20295'
url_armory_other = 'http://realm667.com/index.php/en/armory-mainmenu-157-97317/other-sources-styles-mainmenu-160-29963'

path_tmp = os.path.dirname(__file__) + '/../tmp'

try:
    os.mkdir(path_tmp)
except OSError:
    pass

os.chdir(path_tmp)

for index in [0, 30, 60, 90]:
    url = url_armory_doom.format(index)
    fetch_repository(url)

fetch_repository(url_armory_hh)
fetch_repository(url_armory_other)

file_menu = open('menudef.txt', 'w')
file_repo = open('repository.py', 'w')

for item in repository:
    line_menu = '    Command "{0}", "summon {1}"\n'.format(item[1], item[2])
    file_menu.write(line_menu)

    line_repo = "    ({0}, '{1}'),\n".format(item[0], item[1])
    file_repo.write(line_repo)

file_repo.close()
file_menu.close()

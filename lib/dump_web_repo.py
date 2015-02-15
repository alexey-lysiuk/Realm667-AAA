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


pattern_summon = re.compile(r'Summon:\s*(</strong>|</b>)\s*(&nbsp;\s*)?([^\s][\w\s\[\],-\.\(\)\'/]+)(<strong>|<b>|<br />)', re.UNICODE)
pattern_id_name = re.compile(r'gid=(\d+)(&amp;gt;=)?"(\s+class="doclink")?(\s+target="_self")?>\s*([^\s][\w\s\[\],-\.\(\)\']+)\s*</a>', re.UNICODE)

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
    count = 0

    while True:
        match = pattern_summon.search(html, pos)

        if not match:
            break

        summon = match.group(3).strip(' \r\n')

        match = pattern_id_name.search(html, match.end())

        if not match:
            break

        id = match.group(1)
        name = match.group(5).strip()

        repository.append((id, name, summon))

        pos = match.end()

        count += 1

    if count:
        separator = '--- {0} items ---'.format(count)
        repository.append((-1, separator, separator))

    return count


# Configuration

url_website      = 'http://realm667.com/index.php/en/'
url_armory       = url_website + 'armory-mainmenu-157-97317/'
url_beastiary    = url_website + 'beastiary-mainmenu-136-69621/'
url_item_shop    = url_website + 'item-store-mainmenu-169-61042/'

url_armory_doom  = url_armory + 'doom-style-mainmenu-158-94349'
url_armory_hh    = url_armory + 'heretic-hexen-style-mainmenu-159-20295'
url_armory_other = url_armory + 'other-sources-styles-mainmenu-160-29963'

url_beast_doom   = url_beastiary + 'doom-style-mainmenu-105-73113'
url_beast_hh     = url_beastiary + 'heretic-hexen-style-mainmenu-137-49102'
url_beast_strife = url_beastiary + 'strife-style-mainmenu-173-3492'

url_item_powerup = url_item_shop + 'powerups-a-artifacts-mainmenu-170-4162'
url_item_puzzle  = url_item_shop + 'keys-a-puzzle-mainmenu-171-21592'
url_item_other   = url_item_shop + 'others-mainmenu-172-93727'

urls = [
    url_armory_doom,
    url_armory_hh,
    url_armory_other,
    url_beast_doom,
    url_beast_hh,
    url_beast_strife,
    url_item_powerup,
    url_item_puzzle,
    url_item_other,
]

url_index_template = '?start={0}'
indices_per_page = 30


# Prepare

path_tmp = os.path.dirname(__file__) + '/../tmp'

try:
    os.mkdir(path_tmp)
except OSError:
    pass

os.chdir(path_tmp)

# Fetch asset descriptions from repository

for url in urls:
    index = 0

    while fetch_repository((url + url_index_template).format(index)) > 0:
        index += indices_per_page

# Save gathered asset descriptions

file_menu = open('menudef.txt', 'w')
file_repo = open('repository.py', 'w')

for item in repository:
    line_menu = '    Command "{0}", "summon {1}"\n'.format(item[1], item[2])
    file_menu.write(line_menu)

    line_repo = "    ({0}, '{1}'),\n".format(item[0], item[1])
    file_repo.write(line_repo)

file_repo.close()
file_menu.close()

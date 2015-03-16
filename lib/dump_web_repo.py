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
import urllib2
from HTMLParser import HTMLParser


pattern_summon = re.compile(
    r'Summon:\s*(?:</strong>|</b>)\s*(?:&nbsp;\s*)?'
    r'(\S[\w\s\[\],-.()\'/&;"]+)'
    r'(?:<strong>|<b>|<br />)', re.UNICODE)
pattern_id_name = re.compile(
    r'gid=(\d+)'
    r'(?:&amp;(?:gt;=&amp;)?Itemid=)?"(?:\s+class="doclink")?(?:\s+target="_self")?>(?:<span class="doclink">)?\s*'
    r'(\S[\w\s\[\],-.()\'/&;"]+)'
    r'\s*(?:</span>)?</a>', re.UNICODE)

repository = []


class TestHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._parsing_span = 0
        self._link = None

    def handle_starttag(self, tag, attrs):
        if self._parsing_span:
            if 'a' == tag:
                for attr in attrs:
                    if 'href' == attr[0]:
                        self._link = attr[1]

        if 'span' == tag:
            if self._parsing_span:
                self._parsing_span += 1

            for attr in attrs:
                if 'class' == attr[0] and 'download' in attr[1]:
                    self._parsing_span = 1  # no nested download spans
                    break

    def handle_endtag(self, tag):
        if self._parsing_span and 'span' == tag:
            self._parsing_span -= 1

    def handle_data(self, data):
        if self._link:
            name = data.strip()

            if name.lower().endswith('.zip'):
                name = name[:-4]

            if name:
                match = re.search(r'&gid=(\d+)', self._link)
                if match:
                    gid = match.group(1).rjust(3)
                    print("    ({}, '{}'),".format(gid, name))

            self._link = None


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

##    parser = TestHTMLParser()
##    parser.feed(html)

    pos = 0
    count = 0

    while True:
        match = pattern_summon.search(html, pos)

        if not match:
            break

        summon = match.group(1).strip(' \r\n')

        match = pattern_id_name.search(html, match.end())

        if not match:
            break

        id = match.group(1).rjust(3)
        name = match.group(2).strip()

        if name.lower().endswith('.zip'):
            name = name[:-4]

        repository.append((id, name, summon))

        pos = match.end()

        count += 1

    if count:
        separator = '--- {0} items ---'.format(count)
        repository.append((-1, separator, separator))

    return count


# Configuration

url_website = 'http://realm667.com'
url_index_template = '?start={0}'


# Prepare

path_tmp = (sys.path[0] if sys.path[0] else '.') + '/../tmp'

try:
    os.mkdir(path_tmp)
except OSError:
    pass

os.chdir(path_tmp)

# Gather URLs to fetch from

html_main = urllib2.urlopen(url_website).read()
pattern_repo = r'<a href="([\w./-]+)">Repository</a>'
match_repo = re.search(pattern_repo, html_main, re.IGNORECASE)

if not match_repo:
    print('Error: Failed to fetch repository URL')
    exit(1)

url_repo = '{0}{1}'.format(url_website, match_repo.group(1))
html_repo = urllib2.urlopen(url_repo).read()

def make_url(category, subcategory):
    pattern = r'href="([\w./-]+%s[\w./-]+%s[\w./-]+)"' % (category, subcategory)
    match = re.search(pattern, html_repo)

    if not match:
        print('Error: Failed to fetch URL for {0} - {1}'.format(category, subcategory))
        exit(1)

    return url_website + match.group(1)

urls = [
    make_url('armory', 'doom-style'),
    make_url('armory', 'heretic-hexen-style'),
    make_url('armory', 'other-sources-styles'),

    make_url('beastiary', 'doom-style'),
    make_url('beastiary', 'heretic-hexen-style'),
    make_url('beastiary', 'strife-style'),

    make_url('item-store', 'powerups-a-artifacts'),
    make_url('item-store', 'keys-a-puzzle'),
    make_url('item-store', 'others'),

    make_url('prop-stop', 'technical'),
    make_url('prop-stop', 'vegetation'),
    make_url('prop-stop', 'light-sources'),
    make_url('prop-stop', 'gore-a-corpses'),
    make_url('prop-stop', 'hell-a-magic'),

    make_url('sfx-shoppe', 'elemental-effects'),
    make_url('sfx-shoppe', 'particle-spawners'),
    make_url('sfx-shoppe', 'weather-generators'),
]

# Fetch asset descriptions from repository

for url in urls:
    index = 0

    while True:
        fetched_count = fetch_repository((url + url_index_template).format(index))

        if 0 == fetched_count:
            break

        index += fetched_count

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

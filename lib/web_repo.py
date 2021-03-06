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

import re

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

try:
    # Python 2
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

import utils


# ==============================================================================


class WebRepoHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._parsing_span = 0
        self._link = None
        self._summon_found = False
        self._class_names = None
        self.items = []
        # number of entries, it's not always equal to len(self.items)
        # one entry can contain several items, i.e. more than one archives with WADs
        self.entries_count = 0

        self._parsing_div = 0
        self._preview_link = None

    def handle_starttag(self, tag, attrs):
        if self._parsing_span:
            if 'a' == tag:
                for attr in attrs:
                    if 'href' == attr[0]:
                        self._link = attr[1]

        if self._parsing_div:
            if 'img' == tag:
                for attr in attrs:
                    if 'src' == attr[0]:
                        self._preview_link = attr[1]

        if 'span' == tag:
            if self._parsing_span:
                self._parsing_span += 1

            for attr in attrs:
                if 'class' == attr[0] and 'download' in attr[1]:
                    self._parsing_span = 1  # no nested download spans
                    break
        elif 'div' == tag:
            if self._parsing_div:
                self._parsing_div += 1

            for attr in attrs:
                if 'id' == attr[0] and 'preview' in attr[1]:
                    self._parsing_div = 1  # no nested preview divs
                    break

    def handle_endtag(self, tag):
        if self._parsing_span and 'span' == tag:
            self._parsing_span -= 1
        elif self._parsing_div and 'div' == tag:
            self._parsing_div -= 1

    def handle_data(self, data):
        data = data.strip()

        if self._summon_found:
            self._summon_found = False
            self._class_names = data
            self.entries_count += 1
        elif 'Summon:' == data:
            self._summon_found = True
            self._class_names = None
        elif self._link:
            if data.lower().endswith('.zip'):
                data = data[:-4]

            if data:
                match = re.search(r'&gid=(\d+)', self._link)
                if match:
                    gid = int(match.group(1).rjust(3))
                    self.items.append((gid, data, self._class_names, self._preview_link))

            self._link = None
            self._preview_link = None


# ==============================================================================


_DONT_USE_DUMP = 0
_WRITE_TO_DUMP = 1
_READ_FROM_DUMP = 2

_dump_mode = _DONT_USE_DUMP

if _DONT_USE_DUMP != _dump_mode:
    import shelve


def _fetch_html(url):
    print('Fetching {0}'.format(url))

    if _DONT_USE_DUMP == _dump_mode:
        html_dump = None
    else:
        import platform
        dump_filename = '{}html_dump_{}.db'.format(
            utils.temp_path(), platform.python_version())
        html_dump = shelve.open(dump_filename)

    if _READ_FROM_DUMP == _dump_mode:
        try:
            data = html_dump[url]
            html_dump.close()      # is this really needed?
            return utils.native_str(data)
        except KeyError:
            pass

    data = urlopen(url).read()

    if html_dump is not None:
        html_dump[url] = data
        html_dump.close()

    return utils.native_str(data)


# ==============================================================================


_CONTENT = (
    ('armory', 'doom-style'),
    ('armory', 'heretic-hexen-style'),
    ('armory', 'other-sources-styles'),

    ('beastiary', 'doom-style'),
    ('beastiary', 'heretic-hexen-style'),
    ('beastiary', 'strife-style'),

    ('item-store', 'powerups-a-artifacts'),
    ('item-store', 'keys-a-puzzle'),
    ('item-store', 'others'),

    ('prop-stop', 'technical'),
    ('prop-stop', 'vegetation'),
    ('prop-stop', 'light-sources'),
    ('prop-stop', 'gore-a-corpses'),
    ('prop-stop', 'hell-a-magic'),

    ('sfx-shoppe', 'elemental-effects'),
    ('sfx-shoppe', 'particle-spawners'),
    ('sfx-shoppe', 'weather-generators'),
)

_URL_WEBSITE = 'http://realm667.com'
_URL_INDEX_TEMPLATE = '?start={0}'


def _process_html(data, repository, page_separators):
    parser = WebRepoHTMLParser()
    parser.feed(data)

    repository.extend(parser.items)

    if page_separators and parser.entries_count > 0:
        separator = '--- {0} entries / {1} items ---'.format(
            parser.entries_count, len(parser.items))
        repository.append((0, separator, '---', ''))

    return parser.entries_count


def fetch_repository(page_separators=False):
    """
        Fetch web repository content and return it as a list of 4-tuples:
        [int] asset id
        [str] asset name
        [str] actor class name(s)
        [str] relative link to preview image
    """
    html_main = _fetch_html(_URL_WEBSITE)
    pattern_repo = r'<a href="([\w./-]+)">Repository</a>'
    match_repo = re.search(pattern_repo, html_main, re.IGNORECASE)

    if not match_repo:
        return []

    url_repo = _URL_WEBSITE + match_repo.group(1)
    html_repo = _fetch_html(url_repo)

    repository = []

    for category in _CONTENT:
        pattern = r'href="([\w./-]+%s[\w./-]+%s[\w./-]+)"' % category
        match = re.search(pattern, html_repo)

        if not match:
            continue

        url_template = _URL_WEBSITE + match.group(1) + _URL_INDEX_TEMPLATE
        index = 0

        while True:
            data = _fetch_html(url_template.format(index))
            fetched_count = _process_html(data, repository, page_separators)

            if 0 == fetched_count:
                break

            index += fetched_count

    return repository


# ==============================================================================


if __name__ == '__main__':
    repository = fetch_repository(page_separators=True)
    temp_path = utils.temp_path()

    file_menu = open(temp_path + 'menudef.txt', 'wb')
    file_repo = open(temp_path + 'repository.py', 'wb')

    for item in repository:
        line_menu = '    Command "{0}", "r667aaa {1}"\n'.format(item[1], item[2])
        file_menu.write(utils.binary_str(line_menu))

        line_repo = "    ({:3d}, '{}'),\n".format(item[0], item[1])
        file_repo.write(utils.binary_str(line_repo))

    file_repo.close()
    file_menu.close()

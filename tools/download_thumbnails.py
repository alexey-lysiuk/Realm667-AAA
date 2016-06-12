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

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/../lib'

import utils


REPOSITORY_URL = 'http://www.realm667.com/images/content/repository/'
THUMBNAIL_REGEX = re.compile(r'\((http://(www\.)?realm667\.com/images/content/repository/)(\w+)/(.+)\)\|')

index_path = utils.cache_path() + '..' + os.sep + 'index' + os.sep
thumbnail_path = index_path + 'images' + os.sep


if not os.path.exists(thumbnail_path):
    print("Error: cache was not fetched from Git repository")
    sys.exit(1)

for index_filename in os.listdir(index_path):
    if not index_filename.endswith('.md'):
        continue

    index_filepath = index_path + os.sep + index_filename

    with open(index_filepath) as f:
        content = f.readlines()

    updated_content = []

    for line in content:
        match = THUMBNAIL_REGEX.search(line)

        if match:
            thumbnail_subpath = match.group(3)
            thumbnail_filename = match.group(4)

            try:
                # Download thumbnail
                url = REPOSITORY_URL + thumbnail_subpath + '/' + thumbnail_filename
                url = url.replace(' ', '%20')
                print('Downloading ' + url + '...')
                response = urlopen(url)
                data = response.read()

                # Save thumbnail
                try:
                    os.mkdir(thumbnail_path + thumbnail_subpath)
                except OSError:
                    pass

                thumbnail_filename = thumbnail_filename.replace(' ', '')
                thumbnail_filename = thumbnail_filename.replace('%20', '')
                thumbnail_filename = thumbnail_filename.lower()

                with open(thumbnail_path + thumbnail_subpath + os.sep + thumbnail_filename, 'wb') as f:
                    f.write(data)

                line = THUMBNAIL_REGEX.sub('(images/%s/%s)|' % (thumbnail_subpath, thumbnail_filename), line)

            except:
                print('Error: Failed to download thumbnail')

        updated_content.append(line)

    with open(index_filepath, 'w') as f:
        f.writelines(updated_content)

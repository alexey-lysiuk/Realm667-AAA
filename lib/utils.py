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

import os


def temp_path():
    self_path = os.path.dirname(__file__)

    if not self_path:
        self_path = '.'

    return self_path + '/../tmp/'


def license_header():
    filename = os.path.splitext(__file__)[0] + '.py'

    with open(filename) as f:
        header = []

        while True:
            line = f.readline()

            if line.startswith('#!') or not line.strip():
                continue
            elif line.startswith('#'):
                header.append(line)
            else:
                break

    return header

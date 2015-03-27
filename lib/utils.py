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
import sys


root_path = os.path.dirname(__file__)
root_path = (root_path + os.sep if root_path else '') + os.pardir
root_path = os.path.abspath(root_path) + os.sep


def _sub_path(dirname):
    return root_path + dirname + os.sep


bin_path = _sub_path('bin')
data_path = _sub_path('data')
cache_path = _sub_path('cache')
lib_path = _sub_path('lib')
temp_path = _sub_path('tmp')


def exe_path(tool):
    """ Return absolute path to executable in bin directory by its tool name """
    exe_ext = '.exe' if 'win32' == sys.platform else ''
    return '{}{}.{}{}'.format(bin_path, tool, sys.platform, exe_ext)


# ==============================================================================


_STRING_CODEC = 'iso-8859-1'


def native_str(data):
    need_decode = sys.hexversion >= 0x3000000 \
        and isinstance(data, (bytes, bytearray))
    return data.decode(_STRING_CODEC) if need_decode else data


def binary_str(data):
    need_encode = sys.hexversion >= 0x3000000 \
        and isinstance(data, str)
    return data.encode(_STRING_CODEC) if need_encode else data


# ==============================================================================


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

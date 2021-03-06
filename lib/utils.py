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


MODE_AAA = 1  # An Awesome Awesomeness
MODE_ZDS = 2  # ZDoomed Souls

_mode = MODE_AAA


def mode():
    return _mode


def set_mode(new_mode):
    global _mode
    _mode = new_mode


def is_aaa():
    return mode() == MODE_AAA


def is_zds():
    return mode() == MODE_ZDS


# ==============================================================================


_root_path = os.path.dirname(__file__)
_root_path = (_root_path + os.sep if _root_path else '') + os.pardir
_root_path = os.path.abspath(_root_path) + os.sep


def root_path():
    return _root_path


def _sub_path(dirname):
    return root_path() + dirname + os.sep


_bin_path = _sub_path('bin')
_data_path = _sub_path('data')
_cache_path = _sub_path('cache' + os.sep + 'data')
_lib_path = _sub_path('lib')
_temp_path = _sub_path('tmp')


def bin_path():
    return _bin_path


def data_path():
    return _data_path


def cache_path():
    return _cache_path


def lib_path():
    return _lib_path


def temp_path():
    return _temp_path


def exe_path(tool):
    """ Return absolute path to executable in bin directory by its tool name """
    exe_ext = '.exe' if 'win32' == sys.platform else ''
    return '{}{}.{}{}'.format(bin_path(), tool, sys.platform, exe_ext)


def data_common_path():
    return data_path() + 'common/'


def data_project_path():
    return data_path() + ('aaa' if is_aaa() else 'zds') + '/'


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


def license_header(comment='#'):
    project_name = 'An Awesome Awesomeness' if is_aaa() else 'ZDoomed Souls'
    project_years = '2015, 2016' if is_aaa() else '2016'

    license_pattern = '''{0}
{0}    Realm667 - {1}
{0}    Copyright (C) {2} Alexey Lysiuk
{0}
{0}    This program is free software: you can redistribute it and/or modify
{0}    it under the terms of the GNU General Public License as published by
{0}    the Free Software Foundation, either version 3 of the License, or
{0}    (at your option) any later version.
{0}
{0}    This program is distributed in the hope that it will be useful,
{0}    but WITHOUT ANY WARRANTY; without even the implied warranty of
{0}    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
{0}    GNU General Public License for more details.
{0}
{0}    You should have received a copy of the GNU General Public License
{0}    along with this program.  If not, see <http://www.gnu.org/licenses/>.
{0}
'''

    return license_pattern.format(comment, project_name, project_years)

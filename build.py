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
import sys

if (sys.hexversion < 0x2070000
        or 0x3000000 <= sys.hexversion < 0x3020000):
    print('This script requires Python 2.7 or Python 3.2 and higher')
    exit(1)

# all modules are in the lib directory
sys.path[0] = os.path.dirname(os.path.abspath(__file__)) + '/lib'

import build
build.main()

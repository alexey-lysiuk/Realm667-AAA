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

import zipfile


_FILENAME_PATTERN = 'realm667-aaa.'


class _InternalZipPackager(object):
    def __init__(self, compression):
        self._file = zipfile.ZipFile(_FILENAME_PATTERN + 'pk3', 'w', compression)

    def write(self, filename, arcname):
        """ Put bytes from filename into the archive under the name arcname """
        self._file.write(filename, arcname)

    def writestr(self, arcname, data):
        """ Put data into the archive under the name arcname """
        self._file.writestr(arcname, data)

    def close(self):
        self._file.close()


class DefaultZipPackager(_InternalZipPackager):
    def __init__(self):
        _InternalZipPackager.__init__(self, zipfile.ZIP_DEFLATED)


class UncompressedZipPackager(_InternalZipPackager):
    def __init__(self):
        _InternalZipPackager.__init__(self, zipfile.ZIP_STORED)

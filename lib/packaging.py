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
import shutil
import subprocess
import sys
import tempfile
import zipfile

import utils


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


# ==============================================================================


class _SevenZipPackager(object):
    def __init__(self, extention, args):
        exe_path = '{}/../bin/7za.{}'.format(
            os.path.dirname(__file__), sys.platform)
        exe_path = os.path.abspath(exe_path)

        output_filename = '../../{}{}'.format(_FILENAME_PATTERN, extention)

        self._args = [exe_path, 'a', output_filename]
        self._args += args
        self._args.append('*')

        self._work_dir = tempfile.mkdtemp(prefix='', dir=utils.temp_path())

        try:
            os.remove(output_filename)
        except OSError:
            pass

    def _work_filename(self, arcname):
        return '{}/{}'.format(self._work_dir, arcname)

    def write(self, filename, arcname):
        shutil.copy(filename, self._work_filename(arcname))

    def writestr(self, arcname, data):
        with open(self._work_filename(arcname), 'wb') as f:
            f.write(data)

    def close(self):
        print('Compressing package...')

        current_dir = os.getcwd()
        os.chdir(self._work_dir)

        proc = subprocess.Popen(self._args)
        proc.communicate()

        if 0 == proc.returncode:
            print('')
        else:
            print('\nError: External packager failed')

        os.chdir(current_dir)

        shutil.rmtree(self._work_dir, ignore_errors = True)


class SevenZipPK3Packager(_SevenZipPackager):
    def __init__(self):
        _SevenZipPackager.__init__(self, 'pk3', ('-y', '-tzip', '-mx=9'))


class SevenZipPK7Packager(_SevenZipPackager):
    def __init__(self):
        _SevenZipPackager.__init__(self, 'pk7', ('-y', '-t7z', '-mx=9', '-ms=off'))

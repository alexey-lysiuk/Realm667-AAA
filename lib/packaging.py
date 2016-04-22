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
import shutil
import subprocess
import tempfile
import time
import zipfile

import utils


def _filename_pattern():
    return 'realm667-{}.'.format('aaa' if utils.is_aaa() else 'zds')


def _acrfile_date_time():
    return (2015, 2, 2, 0, 0, 0) if utils.is_aaa() else (2016, 4, 17, 0, 0, 0)


class _InternalZipPackager(object):
    def __init__(self, compression):
        self._file = zipfile.ZipFile(_filename_pattern() + 'pk3', 'w', compression)

    def writestr(self, arcname, data):
        """ Put data into the archive under the name arcname """
        zinfo = zipfile.ZipInfo(arcname, date_time=_acrfile_date_time())
        zinfo.compress_type = self._file.compression
        self._file.writestr(zinfo, data)

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
        output_filename = utils.root_path() + _filename_pattern() + extention

        self._args = [utils.exe_path('7za'), 'a', output_filename]
        self._args += args
        self._args.append('*')

        self._work_dir = tempfile.mkdtemp(prefix='', dir=utils.temp_path())

        try:
            os.remove(output_filename)
        except OSError:
            pass

    def _work_filename(self, arcname):
        return '{}/{}'.format(self._work_dir, arcname)

    def writestr(self, arcname, data):
        work_filename = self._work_filename(arcname)

        with open(work_filename, 'wb') as f:
            f.write(utils.binary_str(data))

        file_time = time.mktime(_acrfile_date_time() + (0, 0, -1))
        os.utime(work_filename, (file_time, file_time))

    def close(self):
        print('Compressing package...')

        current_dir = os.getcwd()
        os.chdir(self._work_dir)

        proc = subprocess.Popen(self._args)
        proc.communicate()

        os.chdir(current_dir)

        shutil.rmtree(self._work_dir, ignore_errors=True)

        if 0 != proc.returncode:
            print('\nError: External packager failed')


class SevenZipPK3Packager(_SevenZipPackager):
    def __init__(self):
        _SevenZipPackager.__init__(self, 'pk3', ('-y', '-tzip', '-mx=9'))


class SevenZipPK7Packager(_SevenZipPackager):
    def __init__(self):
        _SevenZipPackager.__init__(self, 'pk7', ('-y', '-t7z', '-mx=9', '-ms=off'))

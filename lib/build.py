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

import argparse
import io
import os
import random
import zipfile

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

import doomwad
import packaging
import patching
import profiling
import rarfile
import StringIO
import utils

from pk3_to_wad import pk3_to_wad
import repo


# ==============================================================================


def _handle_exception():
    import sys

    if sys.gettrace():
        raise
    else:
        if sys.exc_info()[0] == KeyboardInterrupt:
            print("Stopped by user")
            sys.exit()
        else:
            import traceback

            traceback.print_exc()


# ==============================================================================


def _configure():
    # hard-coded seed helps to have predictable generated names
    random.seed(31337)

    # set current directory to project's root directory
    # in order to make build process portable and self-contained,
    # and to do not store anything in current or user's home/temp directories
    os.chdir(utils.root_path())

    try:
        os.mkdir(utils.cache_path())
    except OSError:
        pass

    rarfile.UNRAR_TOOL = utils.exe_path('unrar')

    parser = argparse.ArgumentParser()

    # Generic arguments
    parser.add_argument(
        '-v', '--verbosity', type=int, choices=range(0, 4), default=0,
        help='set output verbosity level')
    parser.add_argument(
        '--disable-optimization',
        help='disable WAD files optimization', action='store_true')
    parser.add_argument(
        '-c', '--compression', type=str,
        choices=['none', 'default', 'pk3', '7zpk3', 'pk7'],
        help='set output file compression')
    parser.add_argument(
        '-p', '--profiling',
        help='enable Python performance profiling', action='store_true')

    # Operational mode arguments
    parser.add_argument(
        '--zdoomed-souls',
        help='build ZDoomed Souls instead of An Awesome Awesomeness',
        action='store_true')
    parser.add_argument(
        '--check-repo-update',
        help='look for new assets in web repository instead of '
        ' building a package', action='store_true')
    parser.add_argument(
        '--clean-asset-cache',
        help='delete cached assets instead of building a package',
        action='store_true')
    parser.add_argument(
        '-d', '--dry-run',
        help='do all build steps but do not write a package',
        action='store_true')
    parser.add_argument(
        '-s', '--single', type=int, default=0,
        help='build only one repository asset specified by its index')

    # Patching-related arguments
    parser.add_argument(
        '--allow-set-pitch',
        help='allow A_SetPitch() calls in DECORATE',
        action='store_true')
    parser.add_argument(
        '--allow-class-replacement',
        help='allow class replacement in DECORATE',
        action='store_true')
    parser.add_argument(
        '--allow-doomednum',
        help='allow editor number (DoomEdNum) assignment in DECORATE',
        action='store_true')
    parser.add_argument(
        '--png-sprites',
        help='convert all sprites to PNG format',
        action='store_true')
    parser.add_argument(
        '--png-sprites-compression',
        type=int, choices=[value for value in range(-1, 10)], default=-1,
        help='set compression level for sprites in PNG format')

    args = parser.parse_args()

    patching.verbosity_level = args.verbosity
    patching.allow_set_pitch = args.allow_set_pitch
    patching.allow_class_replacement = args.allow_class_replacement
    patching.allow_doomednum = args.allow_doomednum
    patching.enable_optimization = not args.disable_optimization
    patching.png_sprites = args.png_sprites
    patching.png_sprites_compression = args.png_sprites_compression

    if args.zdoomed_souls:
        utils.set_mode(utils.MODE_ZDS)

    return args


# ==============================================================================


_ARCHIVE_ZIP = 'zip'
_ARCHIVE_PK3 = 'pk3'
_ARCHIVE_RAR = 'rar'


def _cached_filename(gid, archive_format):
    return '{:s}{:04d}.{:s}'.format(utils.cache_path(), gid, archive_format)


def _detect_zip_format(data):
    fake_file = StringIO.StringIO(data)
    zip_file = zipfile.ZipFile(fake_file)

    for zipped_file in zip_file.filelist:
        filename = zipped_file.filename.lower()

        if filename.endswith('.pk3') or filename.endswith('.wad'):
            return _ARCHIVE_ZIP

    # No .zip or .wad found inside archive file, probably it's .pk3 by itself
    return _ARCHIVE_PK3


def _prepare_pk3(gid, filename, fatal):
    if not os.path.exists(filename):
        if fatal:
            raise IOError, "File not found " + filename
        else:
            return None

    name = None

    for item in repo.content():
        if item[0] == gid:
            name = item[1]
            break

    assert name

    fake_file = StringIO.StringIO()
    zip_file = zipfile.ZipFile(fake_file, 'w')
    zip_file.write(filename, name + '.pk3')

    return zip_file


def _load_cached(gid, archive_format, fatal=True):
    filename = _cached_filename(gid, archive_format)

    if _ARCHIVE_ZIP == archive_format:
        archiver = zipfile.ZipFile
    elif _ARCHIVE_PK3 == archive_format:
        return _prepare_pk3(gid, filename, fatal)
    elif _ARCHIVE_RAR == archive_format:
        archiver = rarfile.RarFile
    else:
        assert False, 'Unsupported archiver'
        return

    try:
        return archiver(filename)
    except:
        if fatal:
            raise


_URL_PATTERN = 'http://realm667.com/index.php/en/component/docman/?task=doc_download&gid={0}'


def _load_and_cache(gid):
    # Try to load archive file from cache
    cached_file = _load_cached(gid, _ARCHIVE_ZIP, fatal=False)

    if not cached_file:
        cached_file = _load_cached(gid, _ARCHIVE_PK3, fatal=False)

    if not cached_file:
        cached_file = _load_cached(gid, _ARCHIVE_RAR, fatal=False)

    if not cached_file:
        try:
            # Download archive file with given ID
            url = _URL_PATTERN.format(gid)
            response = urlopen(url)
            data = response.read()

            # Detect format of archive file
            if data.startswith(b'PK\003\004') or data.startswith(b'PK00'):
                archive_format = _detect_zip_format(data)
            elif data.startswith(b'Rar!'):
                archive_format = _ARCHIVE_RAR
            else:
                print('Error: Unsupported archive format')
                return

            # Save archive file to cache
            filename = _cached_filename(gid, archive_format)
            with open(filename, 'wb') as cached_file:
                cached_file.write(data)

            cached_file = _load_cached(gid, archive_format)

        except:
            print('Error: Failed to load archive file')
            _handle_exception()

    return cached_file


# ==============================================================================


_wad_filenames = set()


def _unique_wad_filename(original_filename):
    wad_name = os.path.basename(original_filename)

    while wad_name in _wad_filenames:
        name, ext = wad_name.rsplit('.', 1)
        wad_name = '{0}@.{1}'.format(name, ext)

    _wad_filenames.add(wad_name)

    return wad_name


def _store_asset(gid, filename, cached_file, packager):
    with cached_file.open(filename) as wad_file:
        wad_data = wad_file.read()

    if filename.lower().endswith('.pk3'):
        # convert .pk3 to .wad
        wad_data = pk3_to_wad(wad_data)
        wad_filename = filename[:-4] + '.wad'
    else:
        wad_filename = filename

    wad = doomwad.WadFile(wad_data)
    wad.filename = wad_filename

    if not wad.find('DECORATE'):
        print('Warning: No DECORATE lump found in file {0}, '
              'skipping...'.format(filename))
        return

    patching.apply_patch(gid, wad)

    wad_data = io.BytesIO()
    wad.writeto(wad_data)

    if packager:
        wad_filename = _unique_wad_filename(wad_filename)
        packager.writestr(wad_filename, wad_data.getvalue())


def _store_lump(full_path, data_path, packager):
    relative = full_path[len(data_path):]

    optimize = relative.lower().endswith('.txt')
    filemode = 'r' if optimize else 'rb'

    print('Processing {}...'.format(relative))

    with open(full_path, filemode) as f:
        content = f.read()

    if optimize:
        content = patching.optimize_text(content)
    elif relative.endswith('.wad'):
        wad = doomwad.WadFile(content)
        wad.filename = relative

        if wad.find('DECORATE'):
            patching.apply_patch(-1, wad)

        wad_data = io.BytesIO()
        wad.writeto(wad_data)

        content = wad_data.getvalue()

    packager.writestr(relative, content)


def _store_data_lumps(packager, data_path):
    for dirname, _, filenames in os.walk(data_path):
        for filename in filenames:
            full_path = os.path.abspath(dirname + os.sep + filename)
            _store_lump(full_path, data_path, packager)


# ==============================================================================


def _select_packager(compression):
    packagers = {
        # uncompressed output file
        'none':    packaging.UncompressedZipPackager,

        # compressed with Python's internal zlib
        None:      packaging.DefaultZipPackager,
        'default': packaging.DefaultZipPackager,
        'pk3':     packaging.DefaultZipPackager,

        # compressed with external 7-Zip tool
        '7zpk3':   packaging.SevenZipPK3Packager,
        'pk7':     packaging.SevenZipPK7Packager,
    }

    assert compression in packagers
    return packagers[compression]()


def _build(args):
    profiler = profiling.Profiler(args.profiling)
    packager = None if args.dry_run else _select_packager(args.compression)

    excluded_wads = repo.excluded_wads()

    for item in repo.content():
        gid = item[0]
        name = item[1]

        if args.single > 0 and args.single != gid:
            continue

        if gid < 0:
            # excluded asset
            _load_and_cache(-gid)

            if args.verbosity > 0:
                print('Skipping #{:03d} {:s}...'.format(-gid, name))
            continue
        elif 0 == gid:
            # category name
            print('\nProcessing {}...'.format(name))
            continue

        print('Processing #{:03d} {:s}...'.format(gid, name))

        cached_file = _load_and_cache(gid)
        if not cached_file:
            continue

        wad_filenames = []

        for zipped_filename in cached_file.namelist():
            is_asset_file = zipped_filename.lower().endswith(('.wad', '.pk3')) \
                and (gid not in excluded_wads
                     or zipped_filename not in excluded_wads[gid])

            if is_asset_file:
                wad_filenames.append(zipped_filename)

        if not wad_filenames:
            print('Error: Neither WAD nor PK3 files found')

            cached_file.close()
            continue

        for filename in wad_filenames:
            try:
                _store_asset(gid, filename, cached_file, packager)

            except:
                print('Error: Failed to add {0}'.format(filename))
                _handle_exception()
                continue

        cached_file.close()

    if packager:
        print('\nProcessing local data files...')
        _store_data_lumps(packager, utils.data_common_path())
        _store_data_lumps(packager, utils.data_project_path())
        packager.close()

    print('')

    profiler.close()


# ==============================================================================


def _check_repo_update():
    import web_repo
    remote_repo = web_repo.fetch_repository()

    local_ids = {abs(gid) for gid, _ in repo.content() if 0 != gid}
    remote_ids = {gid for gid, _, _, _ in remote_repo}

    new_ids = remote_ids - local_ids

    if new_ids:
        print('\nNew IDs found in web repository:')

        for gid in new_ids:
            name = next((item[1] for item in remote_repo if gid == item[0]))
            print('#{:03d} {:s}'.format(gid, name))
    else:
        print('\nWeb repository has no new assets.')


# ==============================================================================


def _clean_cache():
    # do not remove whole directory as it may contain other files, e.g.
    # when cache was created by cloning git repository with assets

    cache_extensions = ('.' + _ARCHIVE_ZIP, '.' + _ARCHIVE_RAR)
    cache_path = utils.cache_path()

    for filename in os.listdir(cache_path):
        if filename.lower().endswith(cache_extensions):
            os.remove(cache_path + filename)

    print('\nAssets cache cleared.')


# ==============================================================================


def main():
    args = _configure()

    if args.check_repo_update:
        _check_repo_update()
    elif args.clean_asset_cache:
        _clean_cache()
    else:
        _build(args)


if __name__ == '__main__':
    main()

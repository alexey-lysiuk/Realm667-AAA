#!/usr/bin/env python

#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015 Alexey Lysiuk
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
import cStringIO
import os, sys
import random
import traceback
import urllib2
import zipfile

_self_path = os.path.dirname(__file__)
if not _self_path:
    _self_path = '.'
sys.path.append(_self_path + '/lib')

import rarfile
import doomwad
import packaging
import patching
import profiling
from pk3_to_wad import pk3_to_wad
from repo import repository, excluded_wads


# ==============================================================================


def configure():
    # hard-coded seed helps to have predictable generated names
    random.seed(31337)

    # set current directory to directory containing this script
    # in order to make build process portable and self-contained,
    # and to do not store anything in current or user's home/temp directories
    os.chdir(_self_path)

    try:
        os.mkdir('cache')
    except OSError:
        pass

    rarfile.UNRAR_TOOL = '{}/bin/unrar.{}'.format(_self_path, sys.platform)

    parser = argparse.ArgumentParser()

    # Generic arguments
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
        help='set output verbosity level')
    parser.add_argument('--disable-optimization',
        help='disable WAD files optimization', action='store_true')
    parser.add_argument('-c', '--compression', type=str,
        choices = ['none', 'default', 'pk3', '7zpk3', 'pk7'],
        help='set output file compression')
    parser.add_argument('-p', '--profiling',
        help='enable Python performance profiling', action='store_true')

    # Patching-related arguments
    parser.add_argument('--allow-set-pitch',
        help='allow A_SetPitch() calls in DECORATE',
        action='store_true')
    parser.add_argument('--allow-class-replacement',
        help='allow class replacement in DECORATE',
        action='store_true')
    parser.add_argument('--allow-doomednum',
        help='allow editor number (DoomEdNum) assignment in DECORATE',
        action='store_true')
    parser.add_argument('--png-sprites',
        help='convert all sprites to PNG format',
        action='store_true')
    parser.add_argument('--png-sprites-compression',
        type=int, choices=[value for value in range(-1, 10)],
        help='set compression level for sprites in PNG format')

    args = parser.parse_args()

    patching.verbosity_level = args.verbosity
    patching.allow_set_pitch = args.allow_set_pitch
    patching.allow_class_replacement = args.allow_class_replacement
    patching.allow_doomednum = args.allow_doomednum
    patching.enable_optimization = not args.disable_optimization
    patching.png_sprites = args.png_sprites
    patching.png_sprites_compression = args.png_sprites_compression

    return args


# ==============================================================================


_ARCHIVE_ZIP = 'zip'
_ARCHIVE_RAR = 'rar'

def cached_filename(gid, archive_format):
    return 'cache/{:04d}.{:s}'.format(gid, archive_format)

def load_cached(gid, archive_format, fatal = True):
    filename = cached_filename(gid, archive_format)

    if _ARCHIVE_ZIP == archive_format:
        archiver = zipfile.ZipFile
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

def load_and_cache(gid):
    # Try to load archive file from cache
    cached_file = load_cached(gid, _ARCHIVE_ZIP, fatal = False)

    if not cached_file:
        cached_file = load_cached(gid, _ARCHIVE_RAR, fatal = False)

    if not cached_file:
        try:
            # Download archive file with given ID
            url = _URL_PATTERN.format(gid)
            response = urllib2.urlopen(url)
            data = response.read()

            # Detect format of archive file
            if data.startswith('PK\003\004') or data.startswith('PK00'):
                archive_format = _ARCHIVE_ZIP
            elif data.startswith('Rar!'):
                archive_format = _ARCHIVE_RAR
            else:
                print('Error: Unsupported archive format')
                return

            # Save archive file to cache
            filename = cached_filename(gid, archive_format)
            with open(filename, 'wb') as cached_file:
                cached_file.write(data)

            cached_file = load_cached(gid, archive_format)

        except:
            print('Error: Failed to load archive file')
            traceback.print_exc()

    return cached_file


# ==============================================================================


_wad_filenames = set()

def unique_wad_filename(original_filename):
    wad_name = os.path.basename(original_filename)

    while wad_name in _wad_filenames:
        name, ext = wad_name.rsplit('.', 1)
        wad_name  = '{0}@.{1}'.format(name, ext)

    _wad_filenames.add(wad_name)

    return wad_name


def store_asset(gid, filename, cached_file, packager):
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

    wad_data = cStringIO.StringIO()
    wad.writeto(wad_data)

    wad_filename = unique_wad_filename(wad_filename)
    packager.writestr(wad_filename, wad_data.getvalue())


def store_lump(filename, packager):
    filepath = '{0}/data/{1}'.format(_self_path, filename)

    if filename.lower().endswith('.txt'):
        # Optimize text lump
        with open(filepath) as f:
            original = f.read()

        optimized = patching.optimize_text(original)
        packager.writestr(filename, optimized)
    else:
        packager.write(filepath, filename)


# ==============================================================================


def select_packager(compression):
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


def build(args):
    profiler = profiling.Profiler(args.profiling)
    packager = select_packager(args.compression)

    for item in repository:
        gid  = item[0]
        name = item[1]

        if gid < 0:
            if args.verbosity > 0:
                print('Skipping #{:04d}: {:s}...'.format(-gid, name))
            continue

        print('Processing #{:04d}: {:s}...'.format(gid, name))

        cached_file = load_and_cache(gid)
        if not cached_file:
            continue

        wad_filenames = []

        for zipped_filename in cached_file.namelist():
            if zipped_filename.lower().endswith(('.wad', '.pk3')):
                wad_filenames.append(zipped_filename)

        for excluded_wad in excluded_wads:
            if gid == excluded_wad[0]:
                try: wad_filenames.remove(excluded_wad[1])
                except: pass

        if not wad_filenames:
            print('Error: Neither WAD nor PK3 files found')

            cached_file.close()
            continue

        for filename in wad_filenames:
            try:
                store_asset(gid, filename, cached_file, packager)

            except Exception as ex:
                print('Error: Failed to add {0}'.format(filename))
                traceback.print_exc()
                continue

        cached_file.close()

    store_lump('cvarinfo.txt', packager)
    store_lump('keyconf.txt',  packager)
    store_lump('menudef.txt',  packager)

    packager.close()
    profiler.close()


if __name__ == '__main__':
    build(configure())

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
import time
import traceback
import urllib2
import zipfile

self_path = os.path.dirname(__file__)
sys.path.append(self_path + '/lib')

import doomwad
import patching
from pk3_to_wad import pk3_to_wad

from repo import repository, excluded_wads

# Configuration

output_filename = 'realm667-aaa.pk3'

url_download = 'http://realm667.com/index.php/en/component/docman/?task=doc_download&gid={0}'


def configure():
    parser = argparse.ArgumentParser()

    # Generic arguments
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
        help='set output verbosity level')
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

    args = parser.parse_args()

    patching.verbosity_level = args.verbosity
    patching.allow_set_pitch = args.allow_set_pitch
    patching.allow_class_replacement = args.allow_class_replacement
    patching.allow_doomednum = args.allow_doomednum

    global enable_profiling
    enable_profiling = args.profiling

def prepare():
    random.seed(31337)

    try:
        os.remove(output_filename)
    except OSError:
        # TODO: report error
        pass

    try:
        os.mkdir('cache')
    except OSError:
        # TODO: report error
        pass

def add_lump(zip, filename):
    filepath = '{0}/data/{1}'.format(self_path, filename)

    if filename.lower().endswith('.txt'):
        # Optimize text lump
        with open(filepath) as f:
            lines = f.readlines()

        def keep_line(line):
            line = line.strip()
            return len(line) > 0 and not line.startswith('//')

        lines = filter(keep_line, lines)
        lines = map(lambda line: line.strip(), lines)

        zip.writestr(filename, '\n'.join(lines))
    else:
        zip.write(filepath, filename)


wad_filenames = set()

def make_wad_filename(original_filename):
    wad_name = os.path.basename(original_filename)

    while wad_name in wad_filenames:
        name, ext = wad_name.rsplit('.', 1)
        wad_name  = '{0}@.{1}'.format(name, ext)

    wad_filenames.add(wad_name)

    return wad_name


def init_profiling():
    if enable_profiling:
        import cProfile

        global _profiler
        _profiler = cProfile.Profile()
        _profiler.enable()
    else:
        global _start_time
        _start_time = time.clock()

def shutdown_profiling():
    if enable_profiling:
        global _profiler
        _profiler.disable()

        import pstats

        profiling_stream = cStringIO.StringIO()
        ps = pstats.Stats(_profiler, stream=profiling_stream).sort_stats('cumulative')
        ps.print_stats()

        print('\n')
        print(profiling_stream.getvalue())
    else:
        global _start_time
        build_time = time.clock() - _start_time
        print('Completed in {0:.3f} seconds'.format(build_time))


def main():
    configure()
    prepare()

    init_profiling()

    # TODO: add error handling
    output_file = zipfile.ZipFile(output_filename, 'a', zipfile.ZIP_DEFLATED)

    for item in repository:
        id   = item[0]
        name = item[1]

        print('Processing #{:04d}: {:s}...'.format(id, name))

        cached_filename = 'cache/{:04d}.zip'.format(id)
        cached_file = None

        try:
            cached_file = zipfile.ZipFile(cached_filename, 'r')

        except Exception:
            try:
                url = url_download.format(id)
                response = urllib2.urlopen(url)
                data = response.read()

                with open(cached_filename, 'wb') as cached_file:
                    cached_file.write(data)

                cached_file = zipfile.ZipFile(cached_filename, 'r')

            except Exception:
                print('Error: Failed to process resource .ZIP file')
                traceback.print_exc()
                continue

        wad_filenames = []

        for zipped_filename in cached_file.namelist():
            if zipped_filename.lower().endswith(('.wad', '.pk3')):
                wad_filenames.append(zipped_filename)

        for excluded_wad in excluded_wads:
            if id == excluded_wad[0]:
                try: wad_filenames.remove(excluded_wad[1])
                except: pass

        if 0 == len(wad_filenames):
            cached_file.close()

            print('Error: Neither WAD nor PK3 files found')
            continue

        for filename in wad_filenames:
            try:
                wad_file = cached_file.open(filename)
                wad_data = wad_file.read()
                wad_file.close()

                if filename.lower().endswith('.pk3'):
                    wad_data = pk3_to_wad(wad_data)
                    filename = filename[:-4] + '.wad'

                wad = doomwad.WadFile(wad_data)
                wad.filename = filename

                if not wad.find('DECORATE'):
                    print('Warning: No DECORATE lump found in file {0}, skipping...'.format(filename))
                    continue

                patching.apply_patch(id, wad)

                wad_data = cStringIO.StringIO()
                wad.writeto(wad_data)

                output_file.writestr(make_wad_filename(filename), wad_data.getvalue())

            except Exception as ex:
                print('Error: Failed to add {0}'.format(filename))
                traceback.print_exc()
                continue

        cached_file.close()

    add_lump(output_file, 'cvarinfo.txt')
    add_lump(output_file, 'keyconf.txt')
    add_lump(output_file, 'menudef.txt')

    output_file.close()

    shutdown_profiling()

if __name__ == '__main__':
    main()

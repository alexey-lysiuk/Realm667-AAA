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


"""
 This tool analyzes assets cache or generated .pk3
 for duplicate lump and sprite names within WAD files
 It prints result to stdout in 'known issues' markdown format
"""

import os
import re
import shutil
import sys
import zipfile

self_path = os.path.dirname(__file__)
os.chdir(self_path)

import doomwad
from case_insensitive import CaseInsensitiveDict
from patching import actor_stateful_pattern, actor_stateless_pattern, \
    actor_header_regex, line_comment_regex, block_comment_regex
from repo import excluded_wads
from iwad_lumps import *
from iwad_actors import actors_all


excluded_lump_names = [
    # lumps
    'ANIMDEFS',
    'DECALDEF',
    'DECORATE',
    'GLDEFS',
    'KEYCONF',
    'LANGUAGE',
    'LOADACS',
    'LOCKDEFS',
    'SNDINFO',
    'TEXTURES',

    # GLDEFS aliases
    'DOOMDEFS',
    'HTICDEFS',
    'HEXNDEFS',
    'STRFDEFS',

    # markers
    'A_START',
    'A_END',
    'S_START',
    'S_END',
    'SS_START',
    'SS_END',
]

lumps_wads = { }

def find_duplicate_lumps(wad):
    """ Find duplicate lumps in WAD file
        Sprite lumps are not taken into account """
    for namespace in wad.namespaces():
        if doomwad.issrpitenamespace(namespace):
            continue

        for lump in wad.uniquenamespacelumps(namespace):
            if lump.name in excluded_lump_names:
                continue

            if lump.name in lumps_wads \
                and wad.filename not in lumps_wads[lump.name]:
                    lumps_wads[lump.name].append(wad.filename)
            else:
                lumps_wads[lump.name] = [wad.filename]

sprites_wads = { }

def find_duplicate_sprites(wad):
    """ Find duplicate sprites in WAD file (4 characters names) """
    for sprite in wad.spritenames():
        if sprite in sprites_wads:
            sprites_wads[sprite].append(wad.filename)
        else:
            sprites_wads[sprite] = [wad.filename]

actors_wads = CaseInsensitiveDict()

def prepare_decorate(wad):
    decorate_lump = wad.find('DECORATE')

    if not decorate_lump:
        print('No DECORATE lump found in {0}'.format(wad.filename))
        return None

    # prepare DECORATE by removing comments
    decorate = decorate_lump.data
    decorate = line_comment_regex.sub('', decorate)
    decorate = block_comment_regex.sub('', decorate)

    return decorate

def find_duplicate_actors(wad):
    """ Find duplicate actors (classes) in WAD file's DECORATE lump """
    decorate = prepare_decorate(wad)
    actors = actor_header_regex.findall(decorate)

    for dummy, actor in actors:
        if actor in actors_wads:
            actors_wads[actor].append(wad.filename)
        else:
            actors_wads[actor] = [wad.filename]


cache_path = '../cache/'

# Analyze cache if True and generated .pk3 if False
analyze_cache = False


def read_wad(zip_file, filename):
    wad_file = zip_file.open(filename)
    wad_data = wad_file.read()
    wad_file.close()

    return doomwad.WadFile(wad_data)


# Scan cache or generated .pk3

zip_filenames = analyze_cache and os.listdir(cache_path) or ['../realm667-aaa.pk3']

for zip_filename in zip_filenames:
    zip_file = None

    if analyze_cache:
        zip_file = zipfile.ZipFile(cache_path + zip_filename)
        asset_id = int(zip_filename.replace('.zip', ''))
    else:
        zip_file = zipfile.ZipFile(zip_filename)

    for zipped_filename in zip_file.namelist():
        if not zipped_filename.lower().endswith('.wad'):
            continue

        # Check WAD for being excluded

        if analyze_cache:
            excluded = False

            for excluded_wad in excluded_wads:
                if id == excluded_wad[0] and zipped_filename == excluded_wad[1]:
                    excluded = True
                    break

            if excluded:
                continue

        # Scan WAD

        wad = read_wad(zip_file, zipped_filename)
        wad.filename = analyze_cache                               \
            and '[{:04d}] {:s}'.format(asset_id, zipped_filename)  \
            or  zipped_filename

        find_duplicate_lumps(wad)
        find_duplicate_sprites(wad)
        find_duplicate_actors(wad)

    zip_file.close()

# Print names collisions

def print_duplicates(mapping, iwads):
    duplicates = []

    for name in mapping:
        wads = mapping[name]

        for iwad in iwads:
            if name in iwad[1]:
                wads.append(iwad[0])

        if 1 == len(wads):
            continue

        wads.sort(key = lambda name: name.lower())

        duplicates.append('|{0}|{1}||'.format(name, ', '.join(wads)))

    duplicates.sort()

    for dup in duplicates:
        print(dup)

print('\n|Lump|WAD Files|Comments|\n|---|---|---|')
print_duplicates(lumps_wads, (
    ('!DOOM.WAD',     lumps_ultdoom ),
    ('!DOOM2.WAD',    lumps_doom2   ),
    ('!TNT.WAD',      lumps_tnt     ),
    ('!PLUTONIA.WAD', lumps_plutonia),
))

print('\n|Sprite|WAD Files|Comments|\n|---|---|---|')
print_duplicates(sprites_wads, (('!DOOM_ALL.WAD', sprites_doom_all),))

print('\n|Actor|WAD Files|Comments|\n|---|---|---|')
print_duplicates(actors_wads,
    (('!ALL.WAD', [name.lower() for name in actors_all]),))


actor_dump_path = '../tmp/actors/'

def dump_actor(actor, filename, content):
    dump_filename = '{0}{1}_{2}.txt' \
        .format(actor_dump_path, actor, filename[:-4])

    f = open(dump_filename, 'wb')
    f.write(content)
    f.close()

def dump_duplicate_actors():
    # NOTE: implementation ignores internal ZDoom actors at the moment

    if analyze_cache:
        return

    try: shutil.rmtree(actor_dump_path)
    except OSError: pass

    try: os.makedirs(actor_dump_path)
    except OSError: pass

    pk3 = zipfile.ZipFile(zip_filenames[0])
    count = 0

    for actor in actors_wads:
        wad_names = actors_wads[actor]

        if 1 == len(wad_names):
            continue

        for wad_name in wad_names:
            wad = read_wad(pk3, wad_name)
            decorate = prepare_decorate(wad)

            for pattern in (actor_stateless_pattern, actor_stateful_pattern):
                match = re.search(pattern % actor, decorate, re.IGNORECASE | re.DOTALL)

                if match:
                    dump_actor(actor, wad_name, match.group())
                    count += 1
                    break

    print('\nActors written: {0}\n'.format(count))
    pk3.close()

#dump_duplicate_actors()
